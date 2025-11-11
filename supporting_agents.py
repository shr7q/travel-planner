# This module defines supporting sub-agents that perform specialized functions
# These agents work together hierarchically under the root agent defined in `agent.py`.

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from travel_planner.tools import google_searching_agent, location_search_tool

LLM = "gemini-2.0-flash"

# Define a news agent that uses google searching to provide current travel events and news
news_agent = Agent(
    model = LLM,
    name = "news_agent",
    description= "Suggests key travel events and news; uses search for current info.",
    instruction = """
        You are responsible for providing a list of events and news recommendations based on the user's query. 
        Limit the choices to 10 results. You need to use the google_searching_agent tool to search the web for information.
    """,
    tools = [google_searching_agent]
)

# Define a location agent that uses location search to provide places and addresses
location_agent = Agent(
    model = LLM,
    name = "location_agent",
    description= "Suggests key travel events and news; uses search for current info.",
    instruction = """
        You are responsible for making suggestions on actual places based on the user's query. Limit the choices to 10 results.
        Each place must have a name, location, and address.
        You can use the location_tool to find the latitude and longitude of the place and address.
    """,
    tools = [location_search_tool]
)

# Define the travel inspiration agent that uses both news and location agents as tools
travel_inspiration_agent = Agent(
    model = LLM,
    name = "travel_inspiration_agent",
    description= "Inspires users with travel ideas", # May consult news and place agents
    instruction = """
        You are travel inspiration agent who help users find their next big dream vacation destinations.
        Your role and goal is to help the user identify a destination and a few activities at the destination the user is interested in. 
    
        As part of that, user may ask you for general history or knowledge about a destination, in that scenario, answer briefly in the best of your ability, but focus on the goal by relating your answer back to destinations and activities the user may in turn like. Use tools directly when required without asking for feedback from the user. 
        - You will call the two tools `location_agent(inspiration query)` and `news_agent(inspiration query)` when appropriate:
        - Use `news_agent` to provide key events and news recommendations based on the user's query.
        - Use `location_agent` to provide a list of locations or nearby places to famous locations when user asks for it, for example "find hotels near eiffel tower", should return nearby hotels given some user preferences.
        - End with a witty joke only if it is a good one. Keep it light and fun!
    """,
    tools = [AgentTool(agent=news_agent), AgentTool(agent=location_agent)]
)

