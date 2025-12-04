# This Agent you can not changes the state by itself.

import uuid # Used to generate a unique session ID
from google.adk.sessions import InMemorySessionService # in-memory service that stores user data
from google.adk.agents   import Agent
from google.adk.runners  import Runner # connects the session and the agent together
from google.genai import types # tools to define user messages
from dotenv import load_dotenv

load_dotenv() # Loading our API keys

chef = Agent(
    name="InformationAgent",
    model="gemini-2.0-flash",
    instruction="User's favourite colour is {fav_color}, name {name}, and favourite subject: {fav_subject}. Answer questions about it."
)
# The instruction is a prompt template with placeholders (context variables), filled using session state before each invocation


service = InMemorySessionService() # A session backend that stores conversational state in memory

session_id  = str(uuid.uuid4()) #  Generates a unique session ID

# Creates a new session for user
service.create_session(   
    app_name="InformationApp", # which application/agent system this session belongs to 
    user_id="ninad", # which user is engaging in the session - allows for user-specific memory
    session_id=session_id, # unique ID for this specific conversation instance.
    state={"fav_color": "green",                    
           "name": "Ninad Gawade", # state - session memory 
           "fav_subject":"Mathematics"},
)

# our runner - waiter: the manager that coordinates between the chef and the notebook .
waiter = Runner(agent=chef, session_service=service, app_name="InformationApp")

# we now send a message (user message)
msg = types.Content(role="user", parts=[types.Part(text="What is my name and what color do I like? Can you also change my favourite colour to red.")])


for ev in waiter.run(user_id="ninad", session_id=session_id, new_message=msg):
    print(ev)
    if ev.is_final_response() and ev.content and ev.content.parts:
        print(ev.content.parts[0].text) # only prints the final response that has content 
        print("-----------")   

"""#------
1. Runner retrieves session by user_id, session_id
2. Fills placeholders in the prompt with state (green, Ninad Gawade, Mathematics)
3. Calls Gemini - our base LLM
4. Outputs a response
#------
"""

# We now manually fetch the session from memory so we can inspect its state. 
session = service.get_session(app_name="InformationApp", user_id="ninad", session_id=session_id)

# 6️⃣ Print updated state
print("\n📘 Final session state:")
for key, value in session.state.items():
    print(f"{key}: {value}")


# Learning: the model can’t modify the state by itself! So we need a way to be able to parse it!
