# Simple Session Agent

Reference: https://www.youtube.com/watch?v=z8Q3qLi9m78

Google ADK - Session Management Example

## Overview

This agent demonstrates how to use **session state** in Google ADK to provide context to your agent. The agent can access user information stored in session state through template placeholders in the instruction.

## Folder Structure

```
simple_session_agent/
├── __init__.py              # Marks the folder as a Python package
├── agent.py                 # Defines the root_agent with session state placeholders
├── run_agent_with_session.py # Script to run the agent with session state
└── README.md                # This file
```

## Key Concepts

### Session State
- **Session state** is a Python dictionary that stores user-specific information
- It persists across multiple messages in a conversation
- State values can be accessed in agent instructions using `{variable_name}` placeholders

### How It Works

1. **Agent Definition** (`agent.py`):
   - Defines `root_agent` with instruction template containing placeholders like `{name}` and `{preference}`
   - ADK automatically fills these placeholders from session state before each message

2. **Session Creation** (`run_agent_with_session.py`):
   - Creates a session with initial state (name, preferences, etc.)
   - Uses `Runner` to execute the agent with the session
   - The agent can access state values through the placeholders

## How to Run

### Option 1: Run as a Python Script (Recommended for this example)

This demonstrates session state programmatically:

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics/simple_session_agent
python run_agent_with_session.py
```

Or using the virtual environment's Python:

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics
./ninad-adk/bin/python simple_session_agent/run_agent_with_session.py
```

### Option 2: Run with ADK CLI

To run the agent interactively:

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics
adk run simple_session_agent
```

**Note:** When using `adk run`, the session state placeholders will work, but you'll need to initialize the state through the ADK session management system.

### Option 3: Run with ADK Web

To run in the web interface:

```bash
cd /Users/ninad/Documents/git/adk/ninad/ADK_basics
adk web .
```

Then select `simple_session_agent` from the list of agents in the web UI.

## Files Explained

### `agent.py`
- Defines the `root_agent` with instruction template
- Uses `{name}` and `{preference}` placeholders that get filled from session state
- Can be used with `adk run` or `adk web`

### `run_agent_with_session.py`
- Standalone script demonstrating session usage
- Creates a session with initial state
- Uses `Runner` to execute the agent
- Shows how to access session state after execution

## Example Output

When you run `run_agent_with_session.py`, you should see:

```
[Agent response about your name and specialties]
-----------

📘 Final session state:
name: Ninad Gawade
preference: [Your preferences text...]
```

## Customization

To customize the session state, edit `run_agent_with_session.py`:

```python
state_context = {
    "name": "Your Name",
    "preference": "Your preferences or specialties"
}
```

To change the question, modify:

```python
user_message = types.Content(role="user", parts=[types.Part(text="Your question here")])
```

## Requirements

- Google ADK installed
- API key configured in `.env` file (GEMINI_API_KEY or GOOGLE_API_KEY)
- Python 3.12+

## Session State Placeholders

In the agent instruction, you can use:
- `{variable_name}` - Required placeholder (will error if not in state)
- `{variable_name?}` - Optional placeholder (empty string if not in state)

Example:
```python
instruction="User's name is {name} and their preference is {preference?}"
```

## Additional Resources

- [Google ADK Documentation](https://google.github.io/adk-docs)
- Reference Video: https://www.youtube.com/watch?v=z8Q3qLi9m78

