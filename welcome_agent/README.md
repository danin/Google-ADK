# Welcome Agent

Reference: https://www.youtube.com/watch?v=f5Ihdw32tTw

Google ADK

# Folder Structure

The following folder structure helps you set up the basic organization for your agent project. It creates a folder named `multi_tool_agent` and adds three files inside it:

- `__init__.py` (marks the folder as a Python package, allowing you to import its modules elsewhere in your project)
- `agent.py` (this is where you will write the main logic and code for your agent)
- `.env` (a hidden file for storing environment variables, such as API keys or configuration settings, that your agent might need)

🧱 Make sure to have this structure as it is essential (and will also make it easier to build and maintain your agent).

```
multi_tool_agent/
├── __init__.py
├── agent.py
└── .env
```

## Ways to Run Agents:

### 🚀 `adk_run`

- The primary command-line tool to run your agent locally.
- Instantly launches your agent for direct interaction in your terminal.
- **Pirate Mode:** Try running with the pirate flag for a fun, themed experience where your agent talks like a pirate! 🏴‍☠️

>>>> adk run welcome_agent 

### 🌐 `adk_web`

- Spins up a web interface for your agent.
- Lets you chat with your agent in a modern browser UI.
- Great for demos, sharing, or a more visual experience.

>>>> >>>> adk web welcome_agent 

## Inbuilt Conversational Memory

- The agent automatically remembers previous messages in a session.
- Provides context to the AI, making conversations more coherent and context-aware.
- No extra setup needed—memory is managed for you!

---
