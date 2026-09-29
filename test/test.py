"""Tests for the current Potter Airlines code.

These tests follow the rules that are actually present in generate_flights.py,
flight.py, and analysis.py. They do not assume later proposed changes.
"""

import datetime

import pandas as pd

from data.generate_flights import generate_flights
from src.analysis import add_occupancy_rate, filter_flights, get_cheapest_flights
from src.flight import Flight


def check_assertion(function):
    try:
        function()
    except AssertionError:
        return
    raise AssertionError("Expected an AssertionError")


def test_generated_flights():
    """Check every rule currently used by generate_flights.py."""
    flights = generate_flights(100)
    airports = {"YYZ", "PVG", "LAX", "JFK", "LHR",
                "CDG", "HKG", "NRT", "YVR", "SIN"}
    first_date = datetime.datetime(2026, 10, 1)
    last_date = datetime.datetime(2027, 9, 30)

    assert len(flights) == 100
    assert len({flight["flight_number"] for flight in flights}) == 100

    for index, flight in enumerate(flights):
        assert flight["flight_number"] == f"PA{100 + index}"
        assert flight["origin"] in airports
        assert flight["destination"] in airports
        assert flight["origin"] != flight["destination"]

        departure_date = datetime.datetime.strptime(
            flight["departure_date"], "%Y-%m-%d"
        )
        assert first_date <= departure_date <= last_date
        assert 100 <= flight["capacity"] <= 300
        assert 0 <= flight["seats_remaining"] <= flight["capacity"]
        assert 100 <= flight["base_fare"] <= 800


def test_flight_validation():
    """Check the assertions currently present in the Flight constructor."""
    departure = datetime.datetime.today() + datetime.timedelta(days=100)

    check_assertion(
        lambda: Flight("PA100", "YYZ", "YVR", departure, 0, 0, 200)
    )
    check_assertion(
        lambda: Flight("PA100", "YYZ", "YVR", departure, -1, 100, 200)
    )
    check_assertion(
        lambda: Flight("PA100", "YYZ", "YVR", departure, 101, 100, 200)
    )


def test_seat_updates():
    """Check successful and unsuccessful bookings."""
    departure = datetime.datetime.today() + datetime.timedelta(days=100)
    flight = Flight("PA100", "YYZ", "YVR", departure, 10, 100, 200)

    assert flight.has_capacity() is True
    assert flight.update_seats_remaining(0) is False
    assert flight.update_seats_remaining(-1) is False
    assert flight.update_seats_remaining(11) is False
    assert flight.seats_remaining == 10

    assert flight.update_seats_remaining(10) is True
    assert flight.seats_remaining == 0
    assert flight.has_capacity() is False


def test_load_factor_boundaries():
    """Check the exact > 50% and > 10% boundaries in the current code."""
    departure = datetime.datetime.today() + datetime.timedelta(days=100)

    above_half = Flight("PA100", "YYZ", "YVR", departure, 51, 100, 200)
    exactly_half = Flight("PA101", "YYZ", "YVR", departure, 50, 100, 200)
    above_ten = Flight("PA102", "YYZ", "YVR", departure, 11, 100, 200)
    exactly_ten = Flight("PA103", "YYZ", "YVR", departure, 10, 100, 200)

    assert above_half.get_load_factor() == 1.0
    assert exactly_half.get_load_factor() == 1.2
    assert above_ten.get_load_factor() == 1.2
    assert exactly_ten.get_load_factor() == 1.5


def test_seasonal_factors():
    """Check the summer, winter, April, and regular-month factors."""
    def make_flight(month):
        departure = datetime.datetime(2027, month, 15)
        return Flight("PA100", "YYZ", "YVR", departure, 50, 100, 200)

    assert make_flight(7).get_seasonal_factor() == 1.3
    assert make_flight(12).get_seasonal_factor() == 1.5
    assert make_flight(4).get_seasonal_factor() == 1.2
    assert make_flight(3).get_seasonal_factor() == 1.0


def test_time_factors_and_past_flight():
    """Check representative values inside each current time interval."""
    now = datetime.datetime.today()

    five_days = Flight("PA100", "YYZ", "YVR",
                       now + datetime.timedelta(days=5), 50, 100, 200)
    ten_days = Flight("PA101", "YYZ", "YVR",
                      now + datetime.timedelta(days=10), 50, 100, 200)
    thirty_days = Flight("PA102", "YYZ", "YVR",
                         now + datetime.timedelta(days=30), 50, 100, 200)
    ninety_days = Flight("PA103", "YYZ", "YVR",
                         now + datetime.timedelta(days=90), 50, 100, 200)
    past = Flight("PA104", "YYZ", "YVR",
                  now - datetime.timedelta(days=2), 50, 100, 200)

    assert five_days.get_time_factor() == 1.55
    assert ten_days.get_time_factor() == 1.2
    assert thirty_days.get_time_factor() == 1.11
    assert ninety_days.get_time_factor() == 1.0

    try:
        past.get_time_factor()
        assert False, "A departed flight should raise ValueError"
    except ValueError:
        pass


def test_price_equation():
    """Check the pricing equation that is currently implemented."""
    departure = datetime.datetime.today() + datetime.timedelta(days=100)
    flight = Flight("PA100", "YYZ", "YVR", departure, 50, 100, 200)

    expected_price = round(
        flight.base_fare
        * flight.get_load_factor()
        * flight.get_seasonal_factor()
        * flight.get_time_factor(),
        2
    )
    assert flight.get_price() == expected_price


def test_analysis_functions():
    """Check filtering, occupancy, and base-fare ranking."""
    flights = pd.DataFrame({
        "flight_number": ["PA100", "PA101", "PA102"],
        "origin": ["YYZ", "YYZ", "YYZ"],
        "destination": ["YVR", "YVR", "LAX"],
        "departure_date": pd.to_datetime(
            ["2027-02-18", "2027-02-18", "2027-02-18"]
        ),
        "base_fare": [300, 200, 100],
        "seats_remaining": [50, 0, 25],
        "capacity": [100, 100, 100]
    })

    selected = filter_flights(
        flights, "YYZ", "YVR", pd.to_datetime("2027-02-18")
    )
    assert len(selected) == 1
    assert selected.iloc[0]["flight_number"] == "PA100"

    result = add_occupancy_rate(flights.copy())
    assert result.loc[0, "occupancy_rate"] == 0.5
    assert result.loc[1, "occupancy_rate"] == 1.0

    cheapest = get_cheapest_flights(flights, 2)
    assert cheapest["flight_number"].tolist() == ["PA102", "PA101"]


def run_all_tests():
    test_generated_flights()
    test_flight_validation()
    test_seat_updates()
    test_load_factor_boundaries()
    test_seasonal_factors()
    test_time_factors_and_past_flight()
    test_price_equation()
    test_analysis_functions()
    print("All tests passed for the current Potter Airlines code.")


if __name__ == "__main__":
    run_all_tests()
