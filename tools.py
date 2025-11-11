from google.adk.tools.google_search_tool import google_search
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import FunctionTool
from geopy.geocoders import Nominatim
import requests

""""
This module defines all external tools and utility functions used by the travel agents.
# Tools include:
#   - Google Search Tool: to fetch travel-related information.
#   - Location Search Tool: to find nearby attractions using OpenStreetMap APIs.
"""

LLM = "gemini-2.0-flash-001"

# Define the Google searching agent
searching_agent = Agent(
    model=LLM,
    name="google_searching_agent",
    description="An agent providing google search grounding capability.",
    instruction="""
    Answer the user's question directly using google_searching_agent tool; Provide a brief but concise response. 
        Rather than a detail response, provide the immediate actionable item for a tourist or traveler, in a single sentence.
        Do not ask the user to check or look up information for themselves, that's your role; do your best to be informative.
        IMPORTANT: 
        - Always return your response in bullet points
        - Specify what matters to the user
    """,
    tools= [google_search]
)
google_searching_agent = AgentTool(agent = searching_agent)

# Define the location search tool using OpenStreetMap APIs
def get_local_attractions(query:str, location: str, radius: int = 3000, limit: int = 5) -> str:
    """
        Finds nearby places for any text query using ONLY free OpenStreetMap APIs (no API key needed).

        Args:
            query (str): What you’re looking for (e.g., "restaurant", "hospital", "gym", "bar").
            location (str): The city or area to search in.
            radius (int): Search radius in meters (default: 3000).
            limit (int): Number of results to show (default: 5).

        Returns:
            str: List of matching place names and addresses.
    """

    try:
        # Step 1: Geocode the location o get coordinates
        geolocator = Nominatim(user_agent="open_place_finder")
        loc = geolocator.geocode(location)
        if not loc:
            return f"Could not find location: '{location}'."

        # Get latitude and longitude
        lat, lon = loc.latitude, loc.longitude

        # Step 2: Use Overpass API to find places matching the query
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json][timeout:25];
        (
          node["name"~"{query}",i](around:{radius},{lat},{lon});
          node["amenity"~"{query}",i](around:{radius},{lat},{lon});
          node["shop"~"{query}",i](around:{radius},{lat},{lon});
        );
        out body {limit};
        """

        # Make the request to Overpass API
        response = requests.get(overpass_url, params = {'data': overpass_query})
        if response.status_code != 200:
            return f"No results found for '{query}' near '{location}'."

        data = response.json()
        elements = data.get('elements', [])
        if not elements:
            return f"No results found for '{query}' near {location}."

        # Step 3: Parse and format results
        output = [f"Top results for '{query}' near {location}:"]

        # Limit results to the specified limit
        for el in elements[:limit]:
            name = el.get('tags', {}).get("name", "Unknown Place")
            street = el.get('tags', {}).get("addr:street", "")
            city = el.get('tags', {}).get("addr:city", "")
            full_addr = ", ".join(filter(None, [street, city]))
            output.append(f"{name}| {full_addr if full_addr else 'Address not available'}")

        return "\n".join(output)

    except Exception as e:
        # Catch any unexpected issues and return an informative message.
        return f"Error searching for '{query}' near '{location}': {str(e)}"

# Define the location search tool
location_search_tool = FunctionTool(func= get_local_attractions)