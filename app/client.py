import asyncio
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()


async def main():
    client = MultiServerMCPClient(
        {
            # "math": {
            #     "command": "python",
            #     "args": ["mathserver.py"],  # absolute path
            #     "transport": "stdio",
            # },
            "todo": {
                "url": "http://todo-server:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )

    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools = await client.get_tools()
    model = ChatGroq(model="qwen-qwq-32b")

    agent = create_react_agent(model, tools)

    todo_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What are my current todos?"}]}
    )
    print("Single-action response:", todo_response["messages"][-1].content)

    todo_response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Please add a todo for preparing the monthly SRE report, "
                        "then list all my current todos."
                    ),
                }
            ]
        }
    )
    print("Multi-action response:", todo_response["messages"][-1].content)


asyncio.run(main())
