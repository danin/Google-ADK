from dotenv import load_dotenv
load_dotenv()
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from pydantic import BaseModel, Field # Library to define these schematics
from google.adk.tools import google_search
import os

os.environ["OTEL_PYTHON_DISABLED"] = "true"

# Define the output structure
class SummaryOutput(BaseModel):
    place: str = Field(description="The place to travel to.")
    days:  int = Field(description="The number of days to travel for.")
    summary: str = Field(description="A summarized message of the results of the travel planning system.")

# -----------------------
# 1. Parallel Sub-Agents
# -----------------------

hotel_search_agent = Agent(
    name="HotelSearchAgent",
    model="gemini-2.0-flash",
    tools=[google_search],
    description="Searches for hotel options.",
    instruction="""
    You are a hotel booking specialist. Research hotels only.
    """,
    output_key="hotel_options",
)

restaurant_search_agent = Agent(
    name="RestaurantSearchAgent",
    model="gemini-2.0-flash",
    tools=[google_search],
    description="Searches for restaurants.",
    instruction="""
    You are a dining expert. Research restaurants only.
    """,
    output_key="restaurant_options",
)

activities_search_agent = Agent(
    name="ActivitiesSearchAgent",
    model="gemini-2.0-flash",
    tools=[google_search],
    description="Searches for activities.",
    instruction="""
    You are an activities expert. Research activities only.
    """,
    output_key="activity_options",
)

parallel_search_agent = ParallelAgent(
    name="TravelPlanningSystem",
    description="Runs hotel, restaurant, and activity search in parallel.",
    sub_agents=[
        hotel_search_agent,
        restaurant_search_agent,
        activities_search_agent,
    ]
)

# -----------------------
# 2. Summary Agent
# -----------------------

summary_agent = Agent(
    name="SummaryAgent",
    model="gemini-2.0-flash",
    description="Summarizes travel results.",
    instruction="""
    You are a travel planner.

    Combine:
    - hotel_options
    - restaurant_options
    - activity_options

    Create a clean summary with:
    - Top hotel recommendations
    - Best restaurants to try
    - Must-do activities

    Be concise and structured.
    """,
    output_schema=SummaryOutput,
    output_key="summary",
)

# -----------------------
# 3. Root sequential workflow
# -----------------------

root_agent = SequentialAgent(
    name="TravelPlannerRoot",
    description="Runs research in parallel then summarizes.",
    sub_agents=[
        parallel_search_agent,  # Step 1 — runs all 3 in parallel
        summary_agent           # Step 2 — summarize the results
    ]
)
