# 🤖 Agentic AI Travel Planner — Google ADK

> An autonomous AI travel planning agent built with **Google Agent Development Kit (ADK)**.  
> The agent uses 6 custom tools to plan complete trips — flights, hotels, weather, budget, local tips & visa requirements — all in one conversation.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Google ADK](https://img.shields.io/badge/Google_ADK-2.1.0-orange?logo=google)
![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-green?logo=google)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🎯 What It Does

The agent autonomously orchestrates 6 tools to answer a single user request like:

> *"Plan a 5-day mid-range trip from Mumbai to Dubai in July for 2 people"*

And returns a complete, structured trip plan:

| Tool | What it provides |
|------|-----------------|
| ✈️ `search_flights` | Flight options, prices, airlines, duration |
| 🏨 `search_hotels` | Hotels, star rating, amenities, total cost |
| 🌤️ `get_weather_forecast` | 5-day forecast + packing suggestions |
| 💰 `calculate_trip_budget` | Itemised budget with per-person breakdown |
| 🗺️ `get_travel_tips` | Attractions, food, transport, cultural tips |
| 📋 `get_visa_requirements` | Visa type, cost, documents, processing time |

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────┐
│   Google ADK Agent          │
│   Model: Gemini 2.0 Flash   │
│   (Orchestration Layer)     │
└────────────┬────────────────┘
             │  Autonomous tool calls
    ┌────────┼────────┐
    ▼        ▼        ▼
search_   search_  get_weather
flights   hotels   _forecast
    │        │        │
    └────────┼────────┘
             │
    ┌────────┼────────┐
    ▼        ▼        ▼
 get_      calc_   get_visa_
travel_   trip_   require-
 tips     budget   ments
             │
             ▼
    Complete Trip Plan
```

The ADK agent decides **which tools to call**, **in what order**, and **how to combine** the results — no hardcoded logic required.

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/swapnaligavali/adk-travel-agent.git
cd adk-travel-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the demo (no API key needed)
```bash
# Default: Mumbai → Dubai, 5 days, mid-range
python demo.py

# Custom trip
python demo.py --origin "Mumbai" --destination "Amsterdam" --days 7 --style "mid-range" --nationality "Indian"
```

### 4. Run with full ADK + Gemini (requires API key)
```bash
# Set your Google API key
export GOOGLE_API_KEY="your-key-here"

# Launch the ADK web UI
adk web

# Or run in terminal
adk run travel_agent
```

---

## 💬 Example Conversation

```
User: Plan a 5-day budget trip from Mumbai to London in September

Agent: I'll plan your London trip right now! Let me search for flights,
       hotels, check the weather and visa requirements...

       ✈️ FLIGHTS — Mumbai → London
       Best: Air India AI131 | USD 480 | 9h direct

       🏨 HOTELS (5 nights)
       Comfort Inn London — 3⭐ | USD 58/night | Total: USD 290
       ✓ Free cancellation | WiFi, Breakfast

       🌤️ WEATHER — September
       Avg 16°C | Partly cloudy | Pack: Light jacket, umbrella

       💰 BUDGET ESTIMATE
       Total for 1 person: USD 1,240
       (Flights: USD 480 | Hotel: USD 290 | Food + Activities: USD 470)

       📋 VISA — Indian passport → UK
       UK Standard Visitor Visa | USD 115 | 15 days processing
       Apply at: gov.uk/apply-uk-visa

       🗺️ TOP TIPS
       Must see: British Museum, Borough Market, Hyde Park
       Try: Fish & chips, Afternoon tea
       Transport: Oyster card for the Tube
```

---

## 📁 Project Structure

```
adk-travel-agent/
├── travel_agent/
│   ├── __init__.py       # Package entry point
│   ├── agent.py          # ADK agent definition
│   └── tools.py          # 6 tool functions
├── tests/
│   └── test_tools.py     # Pytest test suite (25 tests)
├── demo.py               # CLI demo runner
├── requirements.txt
└── README.md
```

---

## 🧪 Run Tests

```bash
pip install pytest
pytest tests/test_tools.py -v
```

25 tests covering all 6 tools — flights, hotels, weather, budget, tips, and visa requirements.

---

## 🔧 Extend This Project

Ideas to make this more advanced:

- 🔌 **Connect to real APIs** — Skyscanner, Booking.com, OpenWeatherMap, Amadeus
- 🗄️ **Add memory** — ADK's `MemoryService` to remember user preferences across sessions
- 🌐 **Deploy as web app** — FastAPI + ADK's built-in web server
- 📱 **Add WhatsApp bot** — Twilio + ADK for a travel planner on WhatsApp
- 🗣️ **Voice interface** — Google Cloud TTS + STT for voice-based planning

---

## 👩‍💻 About the Author

**Swapnali Gavali** — AI & Agentic AI Engineer

- 🔗 [LinkedIn](https://linkedin.com/in/swapnalingavali)
- 🏅 [Credly — Verified Credentials](https://www.credly.com/users/swapnaligavali)
- 🥇 Google Skills Gold League — 28 badges

> 🌍 Open to AI Engineer & Data Engineer roles in UAE 🇦🇪 and Europe 🇪🇺

---

## 📄 License

MIT License — free to use, modify, and share with attribution.
