"""
demo.py — Run the Travel Planner agent locally (no API key needed for tool demo).

For full Gemini LLM integration, set GOOGLE_API_KEY or GOOGLE_CLOUD_PROJECT.
This script shows tool outputs directly so you can demo the agent's capabilities.

Usage:
    python demo.py
    python demo.py --destination Dubai --days 5
"""

import argparse
import json
from travel_agent.tools import (
    search_flights,
    search_hotels,
    get_weather_forecast,
    get_travel_tips,
    calculate_trip_budget,
    get_visa_requirements,
)


def print_section(title: str, emoji: str = ""):
    width = 60
    print(f"\n{'─' * width}")
    print(f"  {emoji}  {title}")
    print(f"{'─' * width}")


def run_demo(origin: str, destination: str, departure: str, days: int,
             budget_style: str, nationality: str):
    print(f"\n{'═' * 60}")
    print(f"  🤖  AGENTIC AI TRAVEL PLANNER")
    print(f"  Powered by Google ADK  |  Built by Swapnali Gavali")
    print(f"{'═' * 60}")
    print(f"\n  Planning your trip: {origin} → {destination}")
    print(f"  Departure: {departure}  |  Duration: {days} days  |  Style: {budget_style}")

    # ── Flights ───────────────────────────────────────────────────────────────
    print_section("FLIGHTS", "✈️")
    from datetime import datetime, timedelta
    return_date = (datetime.strptime(departure, "%Y-%m-%d") +
                   timedelta(days=days)).strftime("%Y-%m-%d")
    flights = search_flights(origin, destination, departure, return_date)
    best = flights["options"][0]
    print(f"  Best option:  {best['airline']}  {best['flight_number']}")
    print(f"  Departure:    {best['departure']}  →  {best['arrival']}")
    print(f"  Duration:     {best['duration_hours']}h  |  Stops: {best['stops']}")
    print(f"  Price:        USD {best['price_usd']}")
    print(f"\n  All options:")
    for f in flights["options"]:
        stops = "Direct" if f["stops"] == 0 else f"{f['stops']} stop(s)"
        print(f"    • {f['airline']:12s}  USD {f['price_usd']:>8.2f}  {stops}")

    # ── Hotels ────────────────────────────────────────────────────────────────
    print_section("HOTELS", "🏨")
    check_out = return_date
    hotels = search_hotels(destination, departure, check_out)
    for h in hotels["options"]:
        cancel = "✓ Free cancellation" if h["free_cancellation"] else "  No free cancellation"
        stars = "⭐" * h["stars"]
        print(f"  {stars}")
        print(f"  {h['name']}")
        print(f"  USD {h['price_per_night_usd']}/night  ·  Total: USD {h['total_usd']}  ·  Rating: {h['rating']}/5")
        print(f"  {cancel}  ·  {', '.join(h['amenities'][:3])}")
        print()

    # ── Weather ───────────────────────────────────────────────────────────────
    print_section("WEATHER FORECAST", "🌤️")
    weather = get_weather_forecast(destination, departure)
    print(f"  Avg temp: {weather['average_temp_c']}°C  |  Humidity: {weather['humidity']}")
    print(f"\n  5-Day Forecast:")
    for day in weather["5_day_forecast"]:
        print(f"  {day['date']}   {day['high_c']}°C / {day['low_c']}°C   {day['condition']}   🌧 {day['rain_chance_pct']}%")
    print(f"\n  🎒 Pack: {', '.join(weather['packing_suggestions'][:3])}")

    # ── Budget ────────────────────────────────────────────────────────────────
    print_section("BUDGET ESTIMATE", "💰")
    budget = calculate_trip_budget(destination, days, budget_style)
    print(f"  Style: {budget['travel_style'].title()}  |  Duration: {days} days")
    print(f"\n  Daily breakdown:")
    for item, cost in budget["daily_breakdown_usd"].items():
        print(f"    {item.title():18s}  USD {cost:>6.2f}/day")
    print(f"\n  {'Land costs:':22s}  USD {budget['total_land_costs_usd']:>8.2f}")
    print(f"  {'Flights (est.):':22s}  USD {budget['estimated_flights_usd']:>8.2f}")
    print(f"  {'─' * 36}")
    print(f"  {'GRAND TOTAL:':22s}  USD {budget['grand_total_usd']:>8.2f}")
    print(f"  {'Per person:':22s}  USD {budget['per_person_usd']:>8.2f}")
    print(f"\n  💡 {budget['tip']}")

    # ── Tips ──────────────────────────────────────────────────────────────────
    print_section("LOCAL TIPS", "🗺️")
    tips = get_travel_tips(destination)
    print(f"  Currency: {tips['currency']}  |  Language: {tips['language']}")
    print(f"\n  Top Attractions:")
    for a in tips["top_attractions"][:4]:
        print(f"    📍 {a}")
    print(f"\n  Must Try Food:")
    for f in tips["local_food"][:3]:
        print(f"    🍽️  {f}")
    print(f"\n  Cultural Tips:")
    for t in tips["cultural_tips"][:3]:
        print(f"    ℹ️  {t}")

    # ── Visa ──────────────────────────────────────────────────────────────────
    print_section("VISA INFORMATION", "📋")
    visa = get_visa_requirements(nationality, destination)
    print(f"  Visa type:       {visa['visa_type']}")
    print(f"  Cost:            USD {visa['cost_usd']}")
    print(f"  Processing:      {visa['processing_days']} days")
    print(f"  Validity:        {visa['validity']}")
    print(f"  Apply at:        {visa['apply_at']}")
    print(f"\n  Documents needed:")
    for doc in visa["documents_needed"][:4]:
        print(f"    📄 {doc}")
    print(f"\n  💡 {visa['tip']}")

    print(f"\n{'═' * 60}")
    print(f"  ✅  Trip plan complete! Have a great trip to {destination}! 🌍")
    print(f"{'═' * 60}\n")


def main():
    parser = argparse.ArgumentParser(description="AI Travel Planner Demo")
    parser.add_argument("--origin",      default="Mumbai",    help="Departure city")
    parser.add_argument("--destination", default="Dubai",     help="Destination city")
    parser.add_argument("--departure",   default="2026-07-15",help="Departure date YYYY-MM-DD")
    parser.add_argument("--days",        default=5, type=int, help="Trip duration in days")
    parser.add_argument("--style",       default="mid-range", help="budget | mid-range | luxury")
    parser.add_argument("--nationality", default="Indian",    help="Your nationality")
    args = parser.parse_args()

    run_demo(
        origin=args.origin,
        destination=args.destination,
        departure=args.departure,
        days=args.days,
        budget_style=args.style,
        nationality=args.nationality,
    )


if __name__ == "__main__":
    main()
