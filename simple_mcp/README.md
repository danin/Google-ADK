# Simple MCP Agent

This agent demonstrates how to integrate Model Context Protocol (MCP) servers with Google ADK agents. Specifically, it uses the Google Maps MCP server to provide location-based information.

## Overview

This example shows how to:
- Connect to an MCP server using stdio communication
- Use `MCPToolset` to load MCP tools into an ADK agent
- Access Google Maps functionality through the MCP server

## Reference Video

For a detailed walkthrough, see: [YouTube Tutorial](https://www.youtube.com/watch?v=HkzOrj2qeXI&t=1277s)

## Folder Structure

```
simple_mcp/
├── __init__.py
├── agent.py
└── README.md
```

## Prerequisites

- **Node.js and npm**: Required to run MCP servers via `npx`
- **Google Maps API Key**: Get one from [Google Cloud Console](https://console.cloud.google.com/)
- **Python 3.10+**: Required for MCP tool support
- **Google ADK**: Installed in your virtual environment

## Environment Variables

Create a `.env` file in the project root (`/Users/ninad/Documents/git/adk/ninad/ADK_basics/.env`) or in the `simple_mcp` directory with the following:

```env
# Google Maps API Key (required for MCP server)
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here

# Google Gemini API Key (required for ADK agent)
GEMINI_API_KEY=your-gemini-api-key-here
# or
GOOGLE_API_KEY=your-google-api-key-here
```

### Getting a Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Maps JavaScript API** and **Geocoding API**
4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy the API key and add it to your `.env` file

## How to Run

### Option 1: Run with ADK CLI (Interactive)

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics
adk run simple_mcp
```

This will start an interactive CLI session where you can chat with the agent. You can ask questions like:
- "What is the latitude and longitude of the Eiffel Tower?"
- "Find directions from New York to Los Angeles"
- "What's the address of the Golden Gate Bridge?"

### Option 2: Run with ADK Web

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics
adk web .
```

Then open your browser to `http://localhost:8000` and select `simple_mcp` from the list of agents.

### Option 3: Run as Python Script

You can run the agent directly as a Python script:

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics
./ninad-adk/bin/python simple_mcp/agent.py
```

Or if you're in the `simple_mcp` directory:

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics/simple_mcp
../ninad-adk/bin/python agent.py
```

### Option 4: Run Programmatically (Using Runner API)

```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from simple_mcp.agent import root_agent
import uuid

# Create session service
session_service = InMemorySessionService()
session_id = str(uuid.uuid4())
user_id = "user"

# Create session
session_service.create_session(
    app_name="MCPApp",
    user_id=user_id,
    session_id=session_id,
    state={}
)

# Create runner
runner = Runner(
    agent=root_agent,
    session_service=session_service,
    app_name="MCPApp"
)

# Ask a question
user_message = types.Content(
    role="user",
    parts=[types.Part(text="What is the latitude and longitude of the Eiffel Tower?")]
)

# Run agent
for event in runner.run(user_id=user_id, session_id=session_id, new_message=user_message):
    if event.is_final_response() and event.content and event.content.parts:
        print(event.content.parts[0].text)
```

## How It Works

1. **MCP Server Connection**: The code uses `StdioServerParameters` to connect to the Google Maps MCP server via `npx`
2. **MCPToolset**: Wraps the MCP server connection and exposes its tools to ADK
3. **Agent Integration**: The `MCPToolset` is passed to the agent's `tools` parameter
4. **Tool Execution**: When the agent needs location information, it calls the MCP tools automatically

## Code Explanation

```python
# Create MCP toolset connection
maps_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",  # Use npx to run the MCP server
        args=["-y", "@modelcontextprotocol/server-google-maps"],
        env={
            "GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY,
        },
    )
)

# Add MCP tools to agent
root_agent = Agent(
    name="simple_mcp_agent",
    model="gemini-2.0-flash",
    tools=[maps_toolset],  # MCP tools are added here
    ...
)
```

## Example Questions

- "What are the coordinates of the Statue of Liberty?"
- "Find the address of the White House"
- "Get directions from San Francisco to Los Angeles"
- "What's the location of the Great Wall of China?"

## Troubleshooting

### Error: `GOOGLE_MAPS_API_KEY is not set`
**Solution**: Make sure you have created a `.env` file with `GOOGLE_MAPS_API_KEY=your-key-here` in the project root or `simple_mcp` directory.

### Error: `No module named 'mcp'`
**Solution**: Install the MCP Python SDK:
```bash
./ninad-adk/bin/pip install mcp
```

### Error: `npx: command not found`
**Solution**: Install Node.js and npm:
- macOS: `brew install node`
- Linux: `sudo apt-get install nodejs npm`
- Or download from [nodejs.org](https://nodejs.org/)

### Error: `ModuleNotFoundError: No module named 'google.adk.tools.mcp_tool'`
**Solution**: Make sure you have the latest version of Google ADK installed:
```bash
./ninad-adk/bin/pip install --upgrade google-adk
```

### Error: `MCP Tool requires Python 3.10 or above`
**Solution**: Upgrade your Python version to 3.10 or higher. Check your version:
```bash
./ninad-adk/bin/python --version
```

### MCP Server Connection Issues
If the MCP server fails to connect:
1. Verify Node.js is installed: `node --version`
2. Verify npm is installed: `npm --version`
3. Try running the MCP server manually:
   ```bash
   npx -y @modelcontextprotocol/server-google-maps
   ```
4. Check that your Google Maps API key is valid and has the required APIs enabled

## Other MCP Servers

You can use other MCP servers by changing the `StdioServerParameters`. Some examples:

### Filesystem MCP Server

The [Filesystem MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) provides secure file system access. You can configure it using environment variables or command-line arguments.

**Option 1: Using environment variables (recommended)**
```python
import os
from google.adk.tools.mcp_tool import MCPToolset
from mcp import StdioServerParameters

filesystem_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem"],
        env={
            # Specify allowed directories (colon-separated for multiple paths)
            "MCP_ALLOWED_DIRECTORIES": "/path/to/dir1:/path/to/dir2",
            # Optional: Specify read-only directories
            "MCP_READ_ONLY_DIRECTORIES": "/path/to/readonly/dir",
            # Optional: Set log level (DEBUG, INFO, WARN, ERROR)
            "MCP_LOG_LEVEL": "INFO",
        },
    )
)
```

**Option 2: Using command-line arguments**
```python
filesystem_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=[
            "-y", 
            "@modelcontextprotocol/server-filesystem",
            "/path/to/dir1",
            "/path/to/dir2"
        ],
    )
)
```

**Adding to agent:**
```python
root_agent = Agent(
    name="filesystem_agent",
    model="gemini-2.0-flash",
    description="An agent that can read and write files",
    instruction="You can help users read, write, and manage files in allowed directories.",
    tools=[filesystem_toolset],
)
```

### GitHub MCP Server
```python
github_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN"),
        },
    )
)
```

## Additional Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Filesystem MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) - Official filesystem server documentation
- [Smithery - MCP Server Registry](https://smithery.ai/)
- [Google ADK Documentation](https://google.github.io/adk-docs)
- [Reference Video](https://www.youtube.com/watch?v=HkzOrj2qeXI&t=1277s)

