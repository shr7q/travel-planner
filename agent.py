# This is the main agent for the travel planner application.
# RUN PROGRAM WITH THE COMMAND:
#      uv run adk web

from google.adk.agents import Agent
from travel_planner.supporting_agents import travel_inspiration_agent

# Define the main LLM to be used
LLM = "gemini-2.0-flash-001"

# Define the root travel planner agent
root_agent = Agent(
    model = LLM,
    name = "travel_planner_agent",
    description= "A helpful travel planning assistant that helps users plan their trips by providing information and suggestions based on their preferences.",
    instruction = """
    - You are an exclusive travel concierge agent
    - You help users to discover their dream holiday destination and plan their vacation.
    - Use the inspiration_agent to get the best destination, news, places nearby e.g hotels, cafes, etc near attractions and points of interest for the user.
    - You cannot use any tool directly. 
    """,
    sub_agents=[travel_inspiration_agent]
)
