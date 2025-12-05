from google.adk.agents import Agent
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
adk_wiki_tool = LangchainTool(tool=wiki_tool)

root_agent = Agent(
    name="langchain_wiki_agent",
    model="gemini-2.0-flash",
    description="A helpful assistant that can search Wikipedia using LangChain tools",
    instruction="You can greet the user and then search Wikipedia for information.",
    tools=[adk_wiki_tool],
)
