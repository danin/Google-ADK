from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from agent import root_agent
from google.genai import types
import uuid


# Create a session service instance
session_service = InMemorySessionService()

#create a state to provide initial information about the user
state_context = {
    "name": "Ninad Gawade",
    "preference": """
    Experienced engineering leader with deep expertise in distributed systems, cloud security, and scalable software architecture. 
    I have a strong track record of leading high-performing, geo-distributed teams and delivering resilient, customer-focused platforms 
    that scale to meet enterprise demands. Skilled in building systems that are not only robust and performant, but also observable, secure, and cost-efficient.

    Currently exploring the intersection of AI and software engineering—building full-stack applications powered by Retrieval-Augmented Generation (RAG), Google ADK, 
    intelligent agent frameworks like LangChain, LangGraph, LangSmith, and Phidata. Passionate about prompt engineering, orchestration with tools like Replit and N8N,
     and continually deepening my understanding of Transformer architectures and LLM pipelines to stay on the cutting edge of applied AI.
    """
}

SESSION_ID = str(uuid.uuid4())
USER_ID = "Ngawade"
APP_NAME = "Social Media Post Generator"

session = session_service.create_session(
    app_name=APP_NAME, 
    user_id=USER_ID,
    session_id=SESSION_ID, 
    state=state_context
    )

#create a runner to run the agent
runner = Runner(
    agent=root_agent, 
    session_service=session_service, 
    app_name=APP_NAME)

#create a user message to ask the agent a question
user_message = types.Content(role="user", parts=[types.Part(text="What is my name and what is my unique quality? ?")])

for event in runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=user_message):
    if event.is_final_response() and event.content and event.content.parts:
        print(event.content.parts[0].text)
        print("-----------")

print ()
#we now manually fetch the session from memory so we can inspect its state.
session = session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
print("\n📘 Final session state:")
for key, value in session.state.items():
    print(f"{key}: {value}")


