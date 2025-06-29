from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")


@mcp.tool()
async def add(a: int, b: int) -> int:
    """
    Add two numbers
    """

    def addition(a: int, b: int): ...

    return a + b


@mcp.tool()
def multiple(a: int, b: int) -> int:
    """
    multiply two numbers
    """
    return a * b


if __name__ == "__main__":
    # stdio transport protocal
    # use standard input and output to reciee and response tool functions calls
    mcp.run(transport="stdio")
