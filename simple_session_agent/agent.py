from google.adk.agents import Agent 

#load the environment variables
from dotenv import load_dotenv

load_dotenv()

#create a new agent
root_agent = Agent(
    name="simple_session_agent",
    model="gemini-2.0-flash",
    description="A helpful assistant that can answer questions about the user.",
    instruction="""
    You are a helpful assistant that can answer questions about the user.
    
    User information from session state:
    - Name: {name}
    - Preferences/Specialties: {preference}
    
    Use this information to answer questions about the user. If the user asks about their name or specialties, 
    provide the information from the session state above.
    """
)