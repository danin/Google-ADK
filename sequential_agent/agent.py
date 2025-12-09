
from dotenv import load_dotenv
load_dotenv()
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search
from typing import Optional
from google.genai import types
from google.adk.agents.callback_context import CallbackContext







def log_input(callback_context: CallbackContext) -> Optional[types.Content]:
    # Access the initial user content (if present)
    user_content = callback_context.user_content
    if user_content and user_content.parts:
        first_part = user_content.parts[0]
        text = getattr(first_part, "text", None)
    else:
        text = None

    print("User content text:", text)
    print("Current state:", callback_context.state)
    return None


# Recipe Research Agent - Finds ingredients and cooking methods
recipe_research_agent = Agent(
    name="RecipeResearchAgent",
    model="gemini-2.0-flash",
    tools=[google_search], # I have given it the google search tool
    description="An agent that researches recipe ideas and ingredients for a given dish concept",
    instruction="""
    You are a culinary researcher. You will be given a dish concept and you will research:
    - Best ingredients and their combinations
    - Popular cooking methods for this dish
    - Key flavor profiles and techniques
    Provide a summary that will help create a complete recipe.
    """,
    output_key="recipe_research",
    before_agent_callback=log_input,  # logs input
)

# Recipe Creator Agent - Creates the final recipe
recipe_creator_agent = Agent(
    model="gemini-2.0-flash",
    name="RecipeCreatorAgent",
    description="An agent that creates complete recipes with ingredients and cooking instructions",
    instruction="""
    You are a professional chef. Using the research from "recipe_research" output, create a complete recipe that includes:
    - Recipe title and brief description
    - Ingredient list with measurements
    - Step-by-step cooking instructions
    - Cooking time and servings
    - Basic nutritional highlights
    Make it clear and easy to follow for home cooks.
    """,
    output_key="final_recipe",
)

# Recipe Enhancement Agent - Adds tips and variations
recipe_enhancement_agent = Agent(
    model="gemini-2.0-flash",
    name="RecipeEnhancementAgent",
    description="An agent that adds cooking tips and recipe variations",
    instruction="""
    You are a cooking instructor. Using the recipe from "final_recipe" output, enhance it by adding:
    - 3-4 helpful cooking tips
    - 2-3 recipe variations or substitutions
    - Storage and serving suggestions
    
    Format the final output as:
    
    RECIPE: {final_recipe}
    
    COOKING TIPS: [your tips here]
    
    VARIATIONS: [your variations here]
    """,
)

# Main sequential agent
root_agent = SequentialAgent(
    name="RecipeDevelopmentSystem",
    description="A simple system that researches, creates, and enhances recipes",
    sub_agents=[recipe_research_agent, recipe_creator_agent, recipe_enhancement_agent],
)

