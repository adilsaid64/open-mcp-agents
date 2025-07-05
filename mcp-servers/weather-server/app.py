from fastmcp import FastMCP

mcp = FastMCP("Math")


@mcp.tool()
async def get_weather(location: str) -> str:
    """
    Get weather location
    """

    def get_weather_api(location: str) -> str:
        return f"It's always raining in {location}"

    result = get_weather_api(location=location)
    return result


if __name__ == "__main__":
    # streamable-http transport protocal
    mcp.run(host="0.0.0.0", transport="streamable-http", port=8000)
