"""
Tests for Travel Agent tools.
Run with: pytest tests/test_tools.py -v
"""

import pytest
from travel_agent.tools import (
    search_flights,
    search_hotels,
    get_weather_forecast,
    get_travel_tips,
    calculate_trip_budget,
    get_visa_requirements,
)


class TestSearchFlights:
    def test_returns_three_options(self):
        result = search_flights("Mumbai", "Dubai", "2026-07-15")
        assert len(result["options"]) == 3

    def test_sorted_by_price(self):
        result = search_flights("Mumbai", "Dubai", "2026-07-15")
        prices = [o["price_usd"] for o in result["options"]]
        assert prices == sorted(prices)

    def test_round_trip_flag(self):
        result = search_flights("Mumbai", "Dubai", "2026-07-15", return_date="2026-07-20")
        assert result["trip_type"] == "round-trip"

    def test_one_way_flag(self):
        result = search_flights("Mumbai", "Dubai", "2026-07-15")
        assert result["trip_type"] == "one-way"

    def test_business_class_more_expensive(self):
        eco = search_flights("Mumbai", "Dubai", "2026-07-15", travel_class="economy")
        biz = search_flights("Mumbai", "Dubai", "2026-07-15", travel_class="business")
        assert biz["options"][0]["price_usd"] > eco["options"][0]["price_usd"]


class TestSearchHotels:
    def test_returns_options(self):
        result = search_hotels("Dubai", "2026-07-15", "2026-07-20")
        assert len(result["options"]) > 0

    def test_nights_calculated(self):
        result = search_hotels("Dubai", "2026-07-15", "2026-07-20")
        assert result["nights"] == 5

    def test_total_matches_nights(self):
        result = search_hotels("Dubai", "2026-07-15", "2026-07-20")
        for h in result["options"]:
            expected = round(h["price_per_night_usd"] * result["nights"], 2)
            assert abs(h["total_usd"] - expected) < 0.01

    def test_budget_filter(self):
        result = search_hotels("Dubai", "2026-07-15", "2026-07-20", max_budget_per_night_usd=70)
        for h in result["options"]:
            assert h["price_per_night_usd"] <= 70


class TestWeatherForecast:
    def test_five_day_forecast(self):
        result = get_weather_forecast("Dubai", "2026-07-15")
        assert len(result["5_day_forecast"]) == 5

    def test_has_packing_suggestions(self):
        result = get_weather_forecast("London", "2026-07-15")
        assert len(result["packing_suggestions"]) >= 2

    def test_hot_city_high_temp(self):
        result = get_weather_forecast("Dubai", "2026-07-15")
        assert result["average_temp_c"] > 25

    def test_cold_city_low_temp(self):
        result = get_weather_forecast("London", "2026-07-15")
        assert result["average_temp_c"] < 25


class TestTravelTips:
    def test_dubai_attractions(self):
        result = get_travel_tips("Dubai")
        assert "Burj Khalifa" in result["top_attractions"]

    def test_has_required_keys(self):
        result = get_travel_tips("Amsterdam")
        for key in ["top_attractions", "local_food", "transport", "cultural_tips", "currency"]:
            assert key in result

    def test_unknown_city_fallback(self):
        result = get_travel_tips("XYZ Unknown City 999")
        assert len(result["top_attractions"]) > 0


class TestBudgetCalculator:
    def test_luxury_more_than_budget(self):
        budget = calculate_trip_budget("Dubai", 5, "budget")
        luxury = calculate_trip_budget("Dubai", 5, "luxury")
        assert luxury["grand_total_usd"] > budget["grand_total_usd"]

    def test_more_people_more_cost(self):
        solo = calculate_trip_budget("Dubai", 5, "mid-range", 1)
        couple = calculate_trip_budget("Dubai", 5, "mid-range", 2)
        assert couple["grand_total_usd"] > solo["grand_total_usd"]

    def test_has_grand_total(self):
        result = calculate_trip_budget("Dubai", 7, "mid-range")
        assert "grand_total_usd" in result
        assert result["grand_total_usd"] > 0


class TestVisaRequirements:
    def test_indian_to_dubai(self):
        result = get_visa_requirements("Indian", "Dubai")
        assert "eVisa" in result["visa_type"] or "Arrival" in result["visa_type"]

    def test_has_documents_list(self):
        result = get_visa_requirements("Indian", "Germany")
        assert len(result["documents_needed"]) >= 4

    def test_unknown_route_fallback(self):
        result = get_visa_requirements("Martian", "Moon")
        assert "visa_type" in result
