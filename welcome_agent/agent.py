#import the agent from google.adk.agents
from google.adk.agents import Agent
from google.genai import types # For further configuration controls
from dotenv import load_dotenv


load_dotenv() 


#create a new agent
root_agent = Agent(
    name="welcome_agent",
    model="gemini-2.0-flash",
    description="A helpful assistant that can answer questions and help with tasks.",
    instruction="You are a helpful assistant that can greet user in a friendly manner got small kids.",

    generate_content_config = types.GenerateContentConfig(
        temperature=0.2, # More deterministic output, closer to 0 more deterministic it is
        max_output_tokens=250
    )
)




