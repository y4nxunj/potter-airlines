"""

Tests for the updated generate_flights.py file. The tests check that 
the generated flight data meets the specified requirements, including 
the number of flights, required columns, valid flight numbers, valid 
routes, departure dates within the specified range, capacity and seats 
remaining constraints, occupancy rate range, and base fare range.

"""

import datetime
import random

from data.generate_flights import generate_flights


# Generate the test data once so every test uses the same 10,000 flights.
flights = generate_flights(10000)

# Test that the number of generated flights is correct
def test_number_of_flights():
    assert len(flights) == 10000

# Test that the generated flight data contains the required columns
def test_required_columns():
    required_columns = {
        "flight_number",
        "origin",
        "destination",
        "departure_date",
        "base_fare",
        "seats_remaining",
        "capacity"
    }

    for flight in flights:
        assert set(flight.keys()) == required_columns

# Test that the flight numbers are valid and follow the expected format
def test_flight_numbers():
    for flight in flights:
        flight_number = flight["flight_number"]

        assert flight_number.startswith("PA")
        assert flight_number[2:].isdigit()
        assert 100 <= int(flight_number[2:]) <= 299

# Test that the origin and destination airports are valid and different
def test_routes():
    valid_routes = {
        ("YYZ", "JFK"), ("YYZ", "LAX"), ("YYZ", "YVR"),
        ("YYZ", "LHR"), ("YYZ", "PVG"), ("YYZ", "HKG"),
        ("JFK", "YYZ"), ("JFK", "LAX"), ("JFK", "LHR"),
        ("JFK", "CDG"), ("LAX", "YYZ"), ("LAX", "JFK"),
        ("LAX", "NRT"), ("LAX", "HKG"), ("LAX", "SIN"),
        ("YVR", "YYZ"), ("YVR", "NRT"), ("YVR", "HKG"),
        ("LHR", "YYZ"), ("LHR", "JFK"), ("LHR", "CDG"),
        ("CDG", "LHR"), ("CDG", "JFK"), ("PVG", "YYZ"),
        ("PVG", "HKG"), ("PVG", "NRT"), ("PVG", "SIN"),
        ("HKG", "YYZ"), ("HKG", "PVG"), ("HKG", "NRT"),
        ("HKG", "SIN"), ("NRT", "LAX"), ("NRT", "YVR"),
        ("NRT", "HKG"), ("NRT", "SIN"), ("SIN", "HKG"),
        ("SIN", "NRT"), ("SIN", "PVG")
    }

    for flight in flights:
        route = (flight["origin"], flight["destination"])

        assert route in valid_routes
        assert flight["origin"] != flight["destination"]

# Test that the departure dates are within the specified range 
# (October 1, 2026 to September 30, 2027)
def test_departure_dates():
    start_date = datetime.datetime(2026, 10, 1)
    end_date = datetime.datetime(2027, 9, 30)

    for flight in flights:
        departure_date = datetime.datetime.strptime(
            flight["departure_date"], "%Y-%m-%d"
        )
        assert start_date <= departure_date <= end_date

# Test that the capacity and seats remaining are within the specified
# ranges
def test_capacity_and_seats():
    for flight in flights:
        assert 150 <= flight["capacity"] <= 300
        assert 0 <= flight["seats_remaining"] <= flight["capacity"]

# Test that the occupancy rate is within the expected range 
# (0.19 to 0.96)
def test_occupancy_range():
    for flight in flights:
        occupancy_rate = (
            1 - flight["seats_remaining"] / flight["capacity"]
        )

        # A small allowance is used because seats_remaining is rounded.
        assert 0.19 <= occupancy_rate <= 0.96

# Test that the base fare is within the specified range (100 to 800)
def test_base_fare():
    for flight in flights:
        assert 100 <= flight["base_fare"] <= 800

