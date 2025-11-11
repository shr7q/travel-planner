# Travel Agent — Google ADK 
> A modular AI travel planner built with **Google ADK**, demonstrating **multi-agent orchestration**, **tool grounding**, and **real-world travel assistance**.

---

## Overview
This project is an intelligent **travel concierge** that helps users:
- Discover dream destinations
- Find local attractions and hotels
- Explore travel news and events
- Save time on planning an itinerary

It uses **Google ADK agents** powered by **Gemini 2.0 Flash models**, plus **OpenStreetMap (Overpass & Nominatim)** for free location search.

---

## Architecture

```
User → root_agent (travel_planner_agent)
└─ travel_inspiration_agent
├─ news_agent → google_searching_agent
└─ location_agent → location_search_tool
```

- **root_agent**: Main interface handling user queries.  
- **travel_inspiration_agent**: Suggests destinations, activities, and jokes.  
- **news_agent**: Fetches travel events & news.  
- **location_agent**: Finds nearby hotels, cafes, etc.

---

## File Structure

| File | Description |
|------|--------------|
| `agent.py` | Defines root agent and entrypoint |
| `supporting_agents.py` | News, location, and inspiration sub-agents |
| `tools.py` | Google search + OpenStreetMap tools |
| `.env` | File consisting of your gemini_api_key |

---

## Key Features
- Multi-agent orchestration with **sub-agent delegation**
- Real-time **news** and **location** discovery
- Uses **free APIs** (no keys required)
- Clean modular code for extensibility  
- Easily integrate itinerary generation or memory later

---

## Setup & Run

### 1. Clone and install
```bash
cd travel-agent-google-adk
uv init .
uv pip install -r requirements.txt
```
### 2. Run
    uv run adk web
---
    
## Example Prompt

“I want you to plan a 4 day trip for me to go and watch the next UFC event live. I stay in Washington DC and my budget for this trip would be $3000. 
My travel dates are flexible around the event and also make sure to include the local attractions for the rest of the days.”

**Agent Flow:**

1. `travel_inspiration_agent` identifies the user’s goal (attend UFC event) and travel constraints.  
2. Calls `news_agent` → fetches upcoming UFC events and locations.  
3. Selects an event that fits the budget and proximity (e.g., UFC Fight Night in New York City).  
4. Calls `location_agent` → finds nearby hotels and attractions using OpenStreetMap (Overpass API).  
5. Combines results into a 4-day itinerary with estimated budget breakdown.  
6. Responds with destination details, travel suggestions, and a light travel joke.

--- 


