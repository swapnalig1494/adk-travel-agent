"""
Travel Agent Tools — all the functions the ADK agent can call autonomously.
Each tool is a plain Python function; ADK handles the LLM ↔ tool loop.
"""

from __future__ import annotations
import random
from datetime import datetime, timedelta
from typing import Optional


# ── Helper ────────────────────────────────────────────────────────────────────

def _price_jitter(base: float, pct: float = 0.15) -> float:
    """Add ±pct realistic price variation."""
    return round(base * (1 + random.uniform(-pct, pct)), 2)


# ── Tool 1: Search Flights ────────────────────────────────────────────────────

def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    passengers: int = 1,
    travel_class: str = "economy",
) -> dict:
    """
    Search for available flights between two cities.

    Args:
        origin: Departure city or airport code (e.g. "Mumbai", "BOM")
        destination: Arrival city or airport code (e.g. "Dubai", "DXB")
        departure_date: Travel date in YYYY-MM-DD format
        return_date: Return date for round trips (optional)
        passengers: Number of passengers (default 1)
        travel_class: "economy", "business", or "first"

    Returns:
        Dictionary with flight options and prices in USD.
    """
    base_prices = {
        "economy": 350,
        "business": 1200,
        "first": 2800,
    }
    base = base_prices.get(travel_class.lower(), 350)

    # Simulate 3 flight options
    airlines = ["Emirates", "Air India", "IndiGo", "Lufthansa", "Etihad", "KLM"]
    options = []
    for i in range(3):
        airline = airlines[i % len(airlines)]
        price = _price_jitter(base) * passengers
        dep_hour = 6 + i * 4
        duration_h = random.randint(3, 14)
        options.append({
            "flight_number": f"{airline[:2].upper()}{random.randint(100,999)}",
            "airline": airline,
            "departure": f"{departure_date} {dep_hour:02d}:00",
            "arrival": f"{departure_date} {(dep_hour + duration_h) % 24:02d}:30",
            "duration_hours": duration_h,
            "price_usd": round(price, 2),
            "stops": i,
            "class": travel_class,
        })

    result = {
        "route": f"{origin} → {destination}",
        "passengers": passengers,
        "trip_type": "round-trip" if return_date else "one-way",
        "options": sorted(options, key=lambda x: x["price_usd"]),
    }
    if return_date:
        result["return_date"] = return_date
    return result


# ── Tool 2: Search Hotels ─────────────────────────────────────────────────────

def search_hotels(
    city: str,
    check_in: str,
    check_out: str,
    guests: int = 1,
    max_budget_per_night_usd: Optional[float] = None,
) -> dict:
    """
    Search for hotels in a city for given dates.

    Args:
        city: Destination city name
        check_in: Check-in date YYYY-MM-DD
        check_out: Check-out date YYYY-MM-DD
        guests: Number of guests
        max_budget_per_night_usd: Optional max price per night in USD

    Returns:
        Dictionary with hotel options, ratings, and prices.
    """
    try:
        nights = (datetime.strptime(check_out, "%Y-%m-%d") -
                  datetime.strptime(check_in, "%Y-%m-%d")).days
    except ValueError:
        nights = 3

    hotel_data = [
        {"name": f"Grand {city} Palace", "stars": 5, "base_per_night": 220, "amenities": ["Pool", "Spa", "Gym", "Free WiFi", "Breakfast"]},
        {"name": f"{city} Central Hotel", "stars": 4, "base_per_night": 110, "amenities": ["Gym", "Free WiFi", "Restaurant"]},
        {"name": f"Comfort Inn {city}", "stars": 3, "base_per_night": 60,  "amenities": ["Free WiFi", "Breakfast"]},
        {"name": f"{city} Budget Stay",  "stars": 2, "base_per_night": 30,  "amenities": ["Free WiFi"]},
    ]

    options = []
    for h in hotel_data:
        ppn = _price_jitter(h["base_per_night"])
        if max_budget_per_night_usd and ppn > max_budget_per_night_usd:
            continue
        options.append({
            "name": h["name"],
            "stars": h["stars"],
            "price_per_night_usd": round(ppn, 2),
            "total_usd": round(ppn * nights, 2),
            "nights": nights,
            "rating": round(random.uniform(3.8, 4.9), 1),
            "amenities": h["amenities"],
            "free_cancellation": random.choice([True, False]),
        })

    return {
        "city": city,
        "check_in": check_in,
        "check_out": check_out,
        "nights": nights,
        "guests": guests,
        "options": options,
    }


# ── Tool 3: Weather Forecast ──────────────────────────────────────────────────

def get_weather_forecast(city: str, travel_date: str) -> dict:
    """
    Get a weather forecast for a city around a travel date.

    Args:
        city: Destination city name
        travel_date: Date of travel in YYYY-MM-DD format

    Returns:
        Dictionary with temperature, conditions, and packing suggestions.
    """
    # Realistic climate presets per region keyword
    climates = {
        "dubai": {"temp_c": (28, 38), "condition": "Sunny & Hot", "humidity": "High"},
        "london": {"temp_c": (8, 16),  "condition": "Partly Cloudy", "humidity": "Moderate"},
        "paris":  {"temp_c": (10, 20), "condition": "Mild & Overcast", "humidity": "Moderate"},
        "amsterdam": {"temp_c": (7, 15), "condition": "Rainy & Windy", "humidity": "High"},
        "berlin": {"temp_c": (5, 18),  "condition": "Cool & Cloudy", "humidity": "Moderate"},
        "mumbai": {"temp_c": (26, 34), "condition": "Humid & Tropical", "humidity": "Very High"},
        "singapore": {"temp_c": (25, 33), "condition": "Tropical Showers", "humidity": "Very High"},
        "new york": {"temp_c": (5, 22), "condition": "Variable", "humidity": "Moderate"},
    }

    city_lower = city.lower()
    climate = next((v for k, v in climates.items() if k in city_lower),
                   {"temp_c": (18, 28), "condition": "Pleasant", "humidity": "Moderate"})

    lo, hi = climate["temp_c"]
    avg = (lo + hi) // 2

    packing = ["Comfortable walking shoes", "Sunscreen"]
    if hi > 30:
        packing += ["Light breathable clothing", "Sunglasses", "Hat"]
    elif lo < 10:
        packing += ["Warm jacket", "Layers", "Umbrella"]
    else:
        packing += ["Light jacket", "Mix of warm and cool clothes"]

    forecast = []
    for i in range(5):
        date = (datetime.strptime(travel_date, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
        forecast.append({
            "date": date,
            "high_c": hi + random.randint(-3, 3),
            "low_c":  lo + random.randint(-2, 2),
            "condition": climate["condition"],
            "rain_chance_pct": random.randint(5, 60),
        })

    return {
        "city": city,
        "around_date": travel_date,
        "average_temp_c": avg,
        "humidity": climate["humidity"],
        "5_day_forecast": forecast,
        "packing_suggestions": packing,
    }


# ── Tool 4: Travel Tips ───────────────────────────────────────────────────────

def get_travel_tips(destination: str) -> dict:
    """
    Get curated local travel tips, must-see attractions, and cultural advice.

    Args:
        destination: City or country name

    Returns:
        Dictionary with attractions, food, transport, and cultural tips.
    """
    tips_db = {
        "dubai": {
            "top_attractions": ["Burj Khalifa", "Dubai Mall", "Dubai Creek", "Palm Jumeirah", "Gold Souk", "Dubai Frame"],
            "local_food": ["Shawarma", "Al Harees", "Machboos", "Luqaimat", "Camel milk coffee"],
            "transport": ["Dubai Metro (clean & cheap)", "Careem/Uber app", "Water Taxi on the Creek"],
            "cultural_tips": ["Dress modestly in public areas", "Ramadan hours may vary", "Tipping ~10% is appreciated", "Friday is the weekend"],
            "best_areas": ["Downtown Dubai", "Jumeirah Beach", "Deira Old Town", "Dubai Marina"],
            "currency": "AED (UAE Dirham)",
            "language": "Arabic (English widely spoken)",
        },
        "amsterdam": {
            "top_attractions": ["Rijksmuseum", "Anne Frank House", "Van Gogh Museum", "Canal cruise", "Vondelpark", "Heineken Experience"],
            "local_food": ["Stroopwafels", "Herring", "Dutch pancakes", "Bitterballen", "Gouda cheese"],
            "transport": ["GVB trams & buses", "Bicycle rental (everyone cycles!)", "Ferry across IJ river (free)"],
            "cultural_tips": ["Buy an OV-chipkaart for public transport", "Cycle lanes are sacred — stay off them", "Cash often not accepted — bring card"],
            "best_areas": ["Jordaan", "De Pijp", "Centrum", "NDSM Wharf"],
            "currency": "EUR",
            "language": "Dutch (English widely spoken)",
        },
        "london": {
            "top_attractions": ["British Museum", "Tower of London", "Buckingham Palace", "Hyde Park", "Borough Market", "Tate Modern"],
            "local_food": ["Fish & chips", "Full English breakfast", "Afternoon tea", "Chicken tikka masala", "Pie & mash"],
            "transport": ["London Underground (Tube)", "Oyster card or contactless", "Boris bikes (Santander Cycles)"],
            "cultural_tips": ["Queue properly — it's sacred", "Tip 10–15% in restaurants", "Pubs close at 11pm", "Weather changes fast — carry a layer"],
            "best_areas": ["Covent Garden", "Shoreditch", "South Bank", "Notting Hill"],
            "currency": "GBP",
            "language": "English",
        },
    }

    dest_lower = destination.lower()
    tips = next((v for k, v in tips_db.items() if k in dest_lower), {
        "top_attractions": ["City centre", "Local museum", "Historical old town", "Local market"],
        "local_food": ["Try street food", "Visit a local market", "Ask locals for restaurant recommendations"],
        "transport": ["Check Google Maps for local transit options", "Ride-hailing apps usually available"],
        "cultural_tips": ["Research local customs before arrival", "Learn a few basic local phrases", "Respect dress codes at religious sites"],
        "best_areas": ["City centre is usually a great starting point"],
        "currency": "Check XE.com for current rates",
        "language": "Check before you go",
    })

    return {"destination": destination, **tips}


# ── Tool 5: Budget Calculator ─────────────────────────────────────────────────

def calculate_trip_budget(
    destination: str,
    duration_days: int,
    travel_style: str = "mid-range",
    num_people: int = 1,
) -> dict:
    """
    Calculate an estimated total trip budget.

    Args:
        destination: Destination city or country
        duration_days: Number of days for the trip
        travel_style: "budget", "mid-range", or "luxury"
        num_people: Number of travellers

    Returns:
        Itemised budget breakdown in USD.
    """
    daily_costs = {
        "budget":    {"accommodation": 30,  "food": 20,  "transport": 10, "activities": 15, "misc": 10},
        "mid-range": {"accommodation": 100, "food": 50,  "transport": 25, "activities": 40, "misc": 25},
        "luxury":    {"accommodation": 300, "food": 150, "transport": 80, "activities": 120, "misc": 70},
    }

    style = travel_style.lower()
    if style not in daily_costs:
        style = "mid-range"

    costs = daily_costs[style]
    breakdown = {k: round(v * duration_days * num_people, 2) for k, v in costs.items()}
    total_land = sum(breakdown.values())

    # Rough flight estimate
    flight_est = {"budget": 400, "mid-range": 700, "luxury": 2000}.get(style, 700) * num_people

    return {
        "destination": destination,
        "duration_days": duration_days,
        "num_people": num_people,
        "travel_style": style,
        "daily_breakdown_usd": costs,
        "total_land_costs_usd": round(total_land, 2),
        "estimated_flights_usd": flight_est,
        "grand_total_usd": round(total_land + flight_est, 2),
        "per_person_usd": round((total_land + flight_est) / num_people, 2),
        "tip": "Add ~15% buffer for unexpected expenses.",
    }


# ── Tool 6: Visa Requirements ─────────────────────────────────────────────────

def get_visa_requirements(nationality: str, destination: str) -> dict:
    """
    Get visa requirements for a given nationality travelling to a destination.

    Args:
        nationality: Traveller's nationality/passport (e.g. "Indian", "British")
        destination: Destination country or city

    Returns:
        Dictionary with visa type, requirements, and application links.
    """
    # Common Indian passport → destination rules (most common use case)
    visa_rules = {
        ("indian", "dubai"):       {"type": "Visa on Arrival / eVisa", "cost_usd": 90,  "processing_days": 3,  "validity": "30 days", "apply_at": "icp.gov.ae"},
        ("indian", "uae"):         {"type": "Visa on Arrival / eVisa", "cost_usd": 90,  "processing_days": 3,  "validity": "30 days", "apply_at": "icp.gov.ae"},
        ("indian", "germany"):     {"type": "Schengen Visa required",  "cost_usd": 90,  "processing_days": 15, "validity": "90 days", "apply_at": "vfsglobal.com"},
        ("indian", "netherlands"): {"type": "Schengen Visa required",  "cost_usd": 90,  "processing_days": 15, "validity": "90 days", "apply_at": "vfsglobal.com"},
        ("indian", "france"):      {"type": "Schengen Visa required",  "cost_usd": 90,  "processing_days": 15, "validity": "90 days", "apply_at": "vfsglobal.com"},
        ("indian", "uk"):          {"type": "UK Standard Visitor Visa","cost_usd": 115, "processing_days": 15, "validity": "6 months","apply_at": "gov.uk/apply-uk-visa"},
        ("indian", "london"):      {"type": "UK Standard Visitor Visa","cost_usd": 115, "processing_days": 15, "validity": "6 months","apply_at": "gov.uk/apply-uk-visa"},
        ("indian", "singapore"):   {"type": "Visa required (eVisa)",   "cost_usd": 30,  "processing_days": 3,  "validity": "30 days", "apply_at": "mom.gov.sg"},
        ("indian", "usa"):         {"type": "B1/B2 Tourist Visa",      "cost_usd": 185, "processing_days": 60, "validity": "10 years","apply_at": "ustraveldocs.com"},
    }

    nat = nationality.lower()
    dest = destination.lower()

    rule = next(
        (v for (n, d), v in visa_rules.items() if n in nat and d in dest),
        {"type": "Check official government website", "cost_usd": "Varies",
         "processing_days": "Varies", "validity": "Varies",
         "apply_at": "iata.org/en/services/pages/travel-centre"}
    )

    docs_needed = [
        "Valid passport (6+ months validity)",
        "Recent passport-size photographs",
        "Bank statements (last 3 months)",
        "Travel insurance",
        "Flight & hotel bookings confirmation",
        "Employment letter or business registration",
    ]

    return {
        "nationality": nationality,
        "destination": destination,
        "visa_type": rule["type"],
        "cost_usd": rule["cost_usd"],
        "processing_days": rule["processing_days"],
        "validity": rule["validity"],
        "apply_at": rule["apply_at"],
        "documents_needed": docs_needed,
        "tip": "Always apply at least 3–4 weeks before travel to allow buffer time.",
    }
