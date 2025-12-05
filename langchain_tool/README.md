# LangChain Tool Integration

This agent demonstrates how to integrate LangChain tools with Google ADK agents. Specifically, it shows how to use LangChain's Wikipedia search tool within an ADK agent.

## Overview

This example uses:
- **LangChain Community Tools**: `WikipediaQueryRun` for Wikipedia searches
- **ADK LangChainTool Wrapper**: `LangchainTool` to bridge LangChain tools with ADK agents
- **Google ADK Agent**: An agent that can use LangChain tools to answer questions

## Folder Structure

```
langchain_tool/
├── __init__.py
├── agent.py
└── README.md
```

## Key Concepts

### LangChain Tools
LangChain provides a rich ecosystem of tools for various tasks (web search, Wikipedia, calculators, etc.). These tools can be integrated into ADK agents using the `LangchainTool` wrapper.

### ADK LangChainTool Wrapper
The `LangchainTool` class from `google.adk.tools.langchain_tool` allows you to use any LangChain tool with ADK agents. It acts as a bridge between LangChain's tool interface and ADK's tool system.

## How It Works

1. **Import LangChain Tools**: Import the desired tool from `langchain_community.tools` (e.g., `WikipediaQueryRun`)
2. **Create LangChain Tool Instance**: Instantiate the LangChain tool with its required dependencies
3. **Wrap with LangchainTool**: Use `LangchainTool` to wrap the LangChain tool for ADK compatibility
4. **Add to Agent**: Pass the wrapped tool to the ADK agent's `tools` parameter

## Code Explanation

```python
from google.adk.agents import Agent
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Create LangChain Wikipedia tool
wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# Wrap it for ADK compatibility
adk_wiki_tool = LangchainTool(tool=wiki_tool)

# Create agent with the wrapped tool
root_agent = Agent(
    name="langchain_wiki_agent",
    model="gemini-2.0-flash",
    description="A helpful assistant that can search Wikipedia using LangChain tools",
    instruction="You can greet the user and then search Wikipedia for information.",
    tools=[adk_wiki_tool],
)
```

## Requirements

### Python Packages
- `langchain-community`: Provides LangChain community tools (including Wikipedia)
- `google-adk`: Google ADK framework
- `python-dotenv`: For loading environment variables

### Installation

If `langchain-community` is not installed:

```bash
# Activate your virtual environment first
source ninad-adk/bin/activate  # or your venv path

# Install langchain-community
pip install langchain-community
```

Or using the virtual environment's pip directly:

```bash
./ninad-adk/bin/pip install langchain-community
```

### Environment Variables

Create a `.env` file in the project root with your API key:

```env
GEMINI_API_KEY=your-gemini-api-key-here
# or
GOOGLE_API_KEY=your-google-api-key-here
```

## How to Run

### Option 1: Run with ADK CLI (Interactive)

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics
adk run langchain_tool
```

This will start an interactive CLI session where you can chat with the agent.

### Option 2: Run with ADK Web

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics
adk web .
```

Then open your browser to `http://localhost:8000` and select `langchain_tool` from the list of agents.

### Option 3: Run as Python Script (Programmatic)

You can also use the Runner API to run the agent programmatically:

```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from langchain_tool.agent import root_agent
import uuid

# Create session service
session_service = InMemorySessionService()
session_id = str(uuid.uuid4())
user_id = "user"

# Create session
session_service.create_session(
    app_name="LangChainToolApp",
    user_id=user_id,
    session_id=session_id,
    state={}
)

# Create runner
runner = Runner(
    agent=root_agent,
    session_service=session_service,
    app_name="LangChainToolApp"
)

# Ask a question
user_message = types.Content(
    role="user",
    parts=[types.Part(text="What is artificial intelligence?")]
)

# Run agent
for event in runner.run(user_id=user_id, session_id=session_id, new_message=user_message):
    if event.is_final_response() and event.content and event.content.parts:
        print(event.content.parts[0].text)
```

## Example Usage

Once running, you can ask questions like:
- "What is machine learning?"
- "Tell me about Python programming"
- "Search Wikipedia for information about quantum computing"
- "What are the main features of React framework?"

The agent will use the Wikipedia tool to search for information and provide answers.

## Other LangChain Tools

You can integrate other LangChain tools in a similar way. Some examples:

### DuckDuckGo Search
```python
from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()
adk_search_tool = LangchainTool(tool=search_tool)
```

### Arxiv Search
```python
from langchain_community.tools import ArxivQueryRun

arxiv_tool = ArxivQueryRun()
adk_arxiv_tool = LangchainTool(tool=arxiv_tool)
```

### Python REPL
```python
from langchain_experimental.tools import PythonREPLTool

python_tool = PythonREPLTool()
adk_python_tool = LangchainTool(tool=python_tool)
```

## Troubleshooting

### Error: `No module named 'langchain.utilities'`
**Solution**: Use `langchain_community.utilities` instead. The import path changed in newer versions of LangChain.

### Error: `No module named 'langchain_community'`
**Solution**: Install it with `pip install langchain-community`

### Error: `ModuleNotFoundError: No module named 'google.adk.tools.langchain_tool'`
**Solution**: Make sure you have the latest version of Google ADK installed. Update with `pip install --upgrade google-adk`

## Additional Resources

- [Google ADK Documentation](https://google.github.io/adk-docs)
- [LangChain Community Tools](https://python.langchain.com/docs/integrations/tools/)
- [LangChain Wikipedia Tool](https://python.langchain.com/docs/integrations/tools/wikipedia)

