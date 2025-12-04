from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


# ------------------------
# User-defined tools
# ------------------------

def get_contact(person: str) -> dict:
    return {"contact": f"{person}'s number is 12345"}

def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny."

contact_tool = FunctionTool(get_contact)
weather_tool = FunctionTool(get_weather)

# ------------------------
# Build agent
# ------------------------

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",

    description="A helpful assistant that can answer questions and help with tasks using tools.",
    instruction="Use tools when needed.",

    generate_content_config=types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=250,
    ),

    tools=[
        contact_tool,
        weather_tool,
       
    ]
)
