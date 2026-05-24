"""
Agentic AI Travel Planner — built with Google ADK
Author: Swapnali Gavali
GitHub: github.com/swapnaligavali
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from travel_agent.tools import (
    search_flights,
    search_hotels,
    get_weather_forecast,
    get_travel_tips,
    calculate_trip_budget,
    get_visa_requirements,
)

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are an expert AI Travel Planner with deep knowledge of destinations 
worldwide. You help users plan complete, personalised trips by:

1. Understanding their travel dates, budget, and preferences
2. Searching for suitable flights and hotels
3. Checking weather forecasts for their travel period
4. Providing visa requirements for their nationality
5. Calculating a realistic trip budget
6. Sharing local tips, must-see attractions, and cultural advice

Always be warm, enthusiastic, and thorough. When a user gives you a 
destination and dates, proactively use your tools to gather all 
relevant information without waiting to be asked.

Structure your final trip plan clearly with sections:
✈️ Flights | 🏨 Hotels | 🌤️ Weather | 💰 Budget | 🗺️ Tips | 📋 Visa Info
"""

# ── Build the agent ───────────────────────────────────────────────────────────
travel_agent = Agent(
    name="travel_planner",
    model="gemini-2.0-flash",
    description="An agentic AI travel planner that searches flights, hotels, weather, visa requirements, and builds complete trip plans.",
    instruction=SYSTEM_PROMPT,
    tools=[
        FunctionTool(search_flights),
        FunctionTool(search_hotels),
        FunctionTool(get_weather_forecast),
        FunctionTool(get_travel_tips),
        FunctionTool(calculate_trip_budget),
        FunctionTool(get_visa_requirements),
    ],
)

# ADK expects a root_agent export
root_agent = travel_agent
