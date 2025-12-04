from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.agents import Agent
from google.genai import types
from dotenv import load_dotenv
import uuid

# Load environment variables (API keys)
load_dotenv()

# One backend for ALL apps
session_service = InMemorySessionService()

############################################################
# 1️⃣ Career Coach Application
############################################################

CAREER_APP = "CareerCoach"

career_agent = Agent(
    name="CareerCoachAgent",
    model="gemini-2.0-flash",
    instruction="User name is {name}. Give career advice tailored to their background: {background}."
)

career_session_id = str(uuid.uuid4())

session_service.create_session(
    app_name=CAREER_APP,
    user_id="Ninad",
    session_id=career_session_id,
    state={
        "name": "Ninad Gawade",
        "background": "Cloud security and distributed systems"
    }
)

career_runner = Runner(
    agent=career_agent,
    session_service=session_service,
    app_name=CAREER_APP
)


############################################################
# 2️⃣ Social Media Post Generator App
############################################################

SOCIAL_APP = "SocialMediaPostGenerator"

social_agent = Agent(
    name="PostAgent",
    model="gemini-2.0-flash",
    instruction="User name is {name}. Create a catchy LinkedIn post about: {topic}"
)

social_session_id = str(uuid.uuid4())

session_service.create_session(
    app_name=SOCIAL_APP,
    user_id="Ninad",
    session_id=social_session_id,
    state={
        "name": "Ninad",
        "topic": "AI agents and RAG systems"
    }
)

social_runner = Runner(
    agent=social_agent,
    session_service=session_service,
    app_name=SOCIAL_APP
)


############################################################
# 3️⃣ Email Assistant App
############################################################

EMAIL_APP = "EmailAssistant"

email_agent = Agent(
    name="EmailAgent",
    model="gemini-2.0-flash",
    instruction="User name: {name}. Draft a polite email reply for: {email_topic}"
)

email_session_id = str(uuid.uuid4())

session_service.create_session(
    app_name=EMAIL_APP,
    user_id="Ninad",
    session_id=email_session_id,
    state={
        "name": "Ninad",
        "email_topic": "requesting interview rescheduling"
    }
)

email_runner = Runner(
    agent=email_agent,
    session_service=session_service,
    app_name=EMAIL_APP
)


############################################################
# 4️⃣ Interacting with all three apps
############################################################

print("=== CAREER COACH RESPONSE ===")
message = types.Content(role="user", parts=[types.Part(text="What career moves should I consider next?")])
for ev in career_runner.run(user_id="Ninad", session_id=career_session_id, new_message=message):
    if ev.is_final_response() and ev.content:
        print(ev.content.parts[0].text)

print("\n=== SOCIAL POST GENERATOR RESPONSE ===")
message = types.Content(role="user", parts=[types.Part(text="Rewrite a viral version of my post.")])
for ev in social_runner.run(user_id="Ninad", session_id=social_session_id, new_message=message):
    if ev.is_final_response() and ev.content:
        print(ev.content.parts[0].text)

print("\n=== EMAIL ASSISTANT RESPONSE ===")
message = types.Content(role="user", parts=[types.Part(text="Draft a friendly email for me.")])
for ev in email_runner.run(user_id="Ninad", session_id=email_session_id, new_message=message):
    if ev.is_final_response() and ev.content:
        print(ev.content.parts[0].text)
