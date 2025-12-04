from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent 

from dotenv import load_dotenv

load_dotenv()

openai_model = LiteLlm(model="openai/gpt-4o-mini")

root_agent = Agent(
    name="openai_agent",
    model=openai_model,
    description="A helpful assistant that can answer questions and help with tasks.",
    instruction="You are a helpful assistant that can answer questions and help with tasks.",
)