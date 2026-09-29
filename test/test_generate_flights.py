"""Tests for the current generate_flights.py file."""

import datetime

from data.generate_flights import generate_flights


def test_number_of_flights():
    flights = generate_flights(100)

    assert len(flights) == 100


def test_flight_numbers():
    flights = generate_flights(100)
    flight_numbers = []

    for index, flight in enumerate(flights):
        assert flight["flight_number"] == f"PA{100 + index}"
        flight_numbers.append(flight["flight_number"])

    assert len(set(flight_numbers)) == 100


def test_airports():
    flights = generate_flights(100)
    airports = [
        "YYZ", "PVG", "LAX", "JFK", "LHR",
        "CDG", "HKG", "NRT", "YVR", "SIN"
    ]

    for flight in flights:
        assert flight["origin"] in airports
        assert flight["destination"] in airports
        assert flight["origin"] != flight["destination"]


def test_departure_dates():
    flights = generate_flights(100)
    start_date = datetime.datetime(2026, 10, 1)
    end_date = datetime.datetime(2027, 9, 30)

    for flight in flights:
        departure_date = datetime.datetime.strptime(
            flight["departure_date"], "%Y-%m-%d"
        )
        assert start_date <= departure_date <= end_date


def test_capacity_and_seats():
    flights = generate_flights(100)

    for flight in flights:
        assert 100 <= flight["capacity"] <= 300
        assert 0 <= flight["seats_remaining"] <= flight["capacity"]


def test_base_fare():
    flights = generate_flights(100)

    for flight in flights:
        assert 100 <= flight["base_fare"] <= 800


def run_generate_flights_tests():
    test_number_of_flights()
    test_flight_numbers()
    test_airports()
    test_departure_dates()
    test_capacity_and_seats()
    test_base_fare()
    print("All generate_flights tests passed.")


if __name__ == "__main__":
    run_generate_flights_tests()
