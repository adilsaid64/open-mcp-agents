import enum

from fastmcp import FastMCP
from sqlalchemy import TIMESTAMP, Column, Enum, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


class TodoStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(length=256))
    status = Column(Enum(TodoStatus), default=TodoStatus.PENDING)
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


mcp = FastMCP("TodoServer")
DATABASE_URL = "sqlite+aiosqlite:///./todos.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def init_data():
    async with async_session() as session:
        result = await session.execute(Todo.__table__.select())
        todos = result.fetchall()
        if not todos:
            sample_todos = [
                Todo(task="Review PR #102", status=TodoStatus.IN_PROGRESS),
                Todo(task="Update documentation", status=TodoStatus.DONE),
            ]
            session.add_all(sample_todos)
            await session.commit()
            print("Sample todos added.")
        else:
            print("Existing todos found, skipping initial population.")


@mcp.tool()
async def add_todo(task: str, status: str = "pending") -> str:
    """
    Add a new todo task with status (default: pending).
    Allowed statuses: pending, in_progress, done.
    """
    if status not in TodoStatus.__members__:
        return f"Invalid status: {status}. Allowed: pending, in_progress, done."

    async with async_session() as session:
        new_todo = Todo(task=task, status=TodoStatus[status])
        session.add(new_todo)
        await session.commit()
        return f"Added todo: {task} with status: {status}"


@mcp.tool()
async def list_todos() -> list[str]:
    """
    List all todos with their status and last updated timestamp.
    """
    async with async_session() as session:
        result = await session.execute(Todo.__table__.select())
        todos = result.fetchall()
        return [
            f"{row.id}: {row.task} [{row.status}] (Last updated: {row.last_updated})"
            for row in todos
        ]


@mcp.tool()
async def delete_todo(todo_id: int) -> str:
    """
    Delete a todo by ID.
    """
    async with async_session() as session:
        result = await session.execute(
            Todo.__table__.delete().where(Todo.id == todo_id)
        )
        await session.commit()
        if result.rowcount:
            return f"Deleted todo with ID {todo_id}"
        else:
            return f"No todo found with ID {todo_id}"


@mcp.tool()
async def update_todo_status(todo_id: int, status: str) -> str:
    """
    Update the status of a todo by ID.
    Allowed statuses: pending, in_progress, done.
    """
    if status not in TodoStatus.__members__:
        return f"Invalid status: {status}. Allowed: pending, in_progress, done."

    async with async_session() as session:
        result = await session.execute(
            Todo.__table__.update()
            .where(Todo.id == todo_id)
            .values(status=TodoStatus[status])
        )
        await session.commit()
        if result.rowcount:
            return f"Updated todo ID {todo_id} to status: {status}"
        else:
            return f"No todo found with ID {todo_id}"


if __name__ == "__main__":
    import asyncio

    asyncio.run(init_db())
    asyncio.run(init_data())

    mcp.run(host="0.0.0.0", transport="streamable-http", port=8000)
