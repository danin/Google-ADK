"""
Example: ADK agent using a Google Maps MCP server over stdio.

MCP Server links:
  - https://github.com/modelcontextprotocol/servers
  - https://smithery.ai/
"""

import os
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset
from mcp import StdioServerParameters

# Load environment variables from .env (same folder)
load_dotenv()

# Make sure your .env has: GOOGLE_MAPS_API_KEY=your_key_here
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if GOOGLE_MAPS_API_KEY is None:
    raise ValueError("GOOGLE_MAPS_API_KEY is not set")

# Define an MCP toolset wired to the Google Maps MCP server via stdio
maps_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-google-maps"],
        env={
            # This env is passed to the MCP server process
            "GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY,
        },
    )
)

file_system_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/Users/ninad/Documents/git/adk/ninad/ADK_basics"],
    )
)



# Define the root agent that will use the MCP tools
root_agent = Agent(
    name="simple_mcp_agent",
    model="gemini-2.0-flash",
    description="A helpful assistant that can answer questions for GOOGLE MAPS MCP SERVER and FILE SYSTEM MCP SERVER",
    instruction=(
        "You are a helpful assistant who has access to the Google Maps MCP server and FILE SYSTEM MCP SERVER, "
        "so you can answer questions about locations, addresses, and directions. You can also read files from the file system."
    ),
    tools=[maps_toolset, file_system_toolset],
)





if __name__ == "__main__":
    # Minimal smoke test: run one prompt via the agent
    import asyncio

    async def main():
        result = await root_agent.run("What is the latitude and longitude of the Eiffel Tower?")
        print(result)

    asyncio.run(main())
