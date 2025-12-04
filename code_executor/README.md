# Code Executor Agent

An ADK agent that demonstrates code execution capabilities. This agent can write and execute Python code to solve user requests.

## Overview

This agent uses `UnsafeLocalCodeExecutor` to execute Python code in your local environment. The agent can:
- Write Python code to solve problems
- Execute the code automatically
- Return results with explanations
- Handle file outputs through the artifact service

## ⚠️ Security Warning

**`UnsafeLocalCodeExecutor` executes code in your local environment!**

- Only use this with **trusted code** or in **secure environments**
- The agent can execute arbitrary Python code on your machine
- Do not use in production without proper security measures
- Consider using `ContainerCodeExecutor` or `VertexAiCodeExecutor` for production

## Folder Structure

```
code_executor/
├── __init__.py    # Marks the folder as a Python package
├── agent.py       # Agent definition and execution script
└── README.md      # This file
```

## How to Run

### Option 1: Run as a Python Script (Recommended for this example)

This runs the agent with a predefined question:

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics/code_executor
python agent.py
```

Or using the virtual environment's Python:

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics
./ninad-adk/bin/python code_executor/agent.py
```

**What it does:**
- Creates a session
- Asks the agent to compute the sum of squares from 1 to 100
- Executes the Python code
- Prints the result

### Option 2: Run with ADK CLI (Interactive)

To run the agent interactively:

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics
adk run code_executor
```

Then you can ask questions like:
- "Write Python code to calculate the factorial of 10"
- "Create a function to find prime numbers up to 50"
- "Plot a simple graph of y = x^2"

### Option 3: Run with ADK Web

To run in the web interface:

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics
adk web .
```

Then select `code_executor` from the list of agents in the web UI at `http://localhost:8000`.

## Requirements

- Google ADK installed
- API key configured in `.env` file:
  ```env
  GEMINI_API_KEY=your-api-key-here
  ```
  Or:
  ```env
  GOOGLE_API_KEY=your-api-key-here
  ```
- Python 3.12+

## How It Works

1. **Code Executor Setup**: Uses `UnsafeLocalCodeExecutor` to execute Python code locally
2. **Agent Definition**: Creates an agent with `code_executor` parameter
3. **Session Management**: Sets up session and artifact services
4. **Code Execution**: When the agent writes code, it's automatically executed
5. **Result Handling**: Execution results are incorporated into the agent's response

## Key Components

### Code Executor
- **`UnsafeLocalCodeExecutor`**: Executes code in the current Python environment
- Detects code blocks in agent responses (marked with ````python` delimiters)
- Executes the code and captures stdout/stderr
- Returns results back to the agent

### Artifact Service
- **`InMemoryArtifactService`**: Required for code executors
- Handles file outputs from code execution (CSV files, images, etc.)
- Stores artifacts in memory (not persistent)

### Session Service
- **`InMemorySessionService`**: Manages conversation state
- Stores session history and context

## Example Usage

When you ask the agent:
```
"Write Python code to compute the sum of squares from 1 to 100, run it, and tell me the result."
```

The agent will:
1. Generate Python code:
   ```python
   sum_squares = sum(i**2 for i in range(1, 101))
   print(sum_squares)
   ```

2. Execute the code automatically

3. Return the result:
   ```
   The sum of squares from 1 to 100 is 338350.
   ```

## Customization

### Change the Question

Edit `agent.py` and modify the `user_message`:

```python
user_message = types.Content(
    role="user",
    parts=[types.Part(text="Your question here")]
)
```

### Use Different Code Executors

For production, consider:
- **`ContainerCodeExecutor`**: Executes code in Docker containers (more secure)
- **`VertexAiCodeExecutor`**: Uses Google Cloud's Vertex AI code execution (cloud-based)

## Code Execution Delimiters

The code executor looks for code blocks with these delimiters:
- ````python\n` ... `\n````
- ````tool_code\n` ... `\n````

The agent instruction tells it to use ````python` delimiters.

## Limitations

- **Security**: `UnsafeLocalCodeExecutor` has no sandboxing
- **State**: Code execution is not stateful by default
- **File Handling**: Files created during execution are managed by the artifact service
- **Errors**: Code execution errors are captured and returned to the agent

## Additional Resources

- [Google ADK Documentation](https://google.github.io/adk-docs)
- [Code Executors Documentation](https://google.github.io/adk-docs/code-execution/code-executor/)

