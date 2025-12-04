from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.code_executors import UnsafeLocalCodeExecutor
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types
import uuid

load_dotenv()

# 1) Configure the code executor for local execution
# WARNING: UnsafeLocalCodeExecutor executes code in your local environment
# Only use this for trusted code or in secure environments
code_executor = UnsafeLocalCodeExecutor()

# 2) Define an agent that is allowed to execute code
root_agent = Agent(
    model="gemini-2.0-flash",  # Using gemini-2.0-flash (gemini-2.5-flash may not be available)
    name="code_exec_demo_agent",
    instruction=(
        "You are a helpful coding assistant. "
        "When useful, write and execute Python code to solve "
        "the user's request and then explain the result in natural language. "
        "Use code blocks with ```python delimiters when writing code."
    ),
    description="A helpful coding assistant that can write and execute Python code to solve the user's request.",
    code_executor=code_executor,
)

# 3) Set up session service and create a session
session_service = InMemorySessionService()
session_id = str(uuid.uuid4())
user_id = "user"

session_service.create_session(
    app_name="CodeExecutorApp",
    user_id=user_id,
    session_id=session_id,
    state={}
)

# 4) Create artifact service (required for code executors to handle file outputs)
artifact_service = InMemoryArtifactService()

# 5) Create a runner
runner = Runner(
    agent=root_agent,
    session_service=session_service,
    artifact_service=artifact_service,
    app_name="CodeExecutorApp"
)

# 6) Ask the agent a question that benefits from code execution
user_message = types.Content(
    role="user",
    parts=[types.Part(text=(
        "Write Python code to compute the sum of squares from 1 to 100, "
        "run it, and tell me the result."
    ))]
)

# 7) Run the agent and print responses
print("=== Agent response ===")
for event in runner.run(user_id=user_id, session_id=session_id, new_message=user_message):
    if event.is_final_response() and event.content and event.content.parts:
        print(event.content.parts[0].text)
        print("\n" + "="*50)
