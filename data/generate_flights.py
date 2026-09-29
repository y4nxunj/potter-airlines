import random
import pandas as pd
import os
from datetime import datetime, timedelta


random.seed(42)


def generate_flights(number_of_flights=10000):

    airports = [
        "YYZ", "PVG", "LAX", "JFK", "LHR", "CDG",
        "HKG", "NRT", "YVR", "SIN"
    ]

    # Common Potter Airlines routes
    # Popular routes appear more often in this list
    routes = [
        ("YYZ", "JFK"),
        ("YYZ", "JFK"),
        ("YYZ", "LAX"),
        ("YYZ", "LAX"),
        ("YYZ", "YVR"),
        ("YYZ", "YVR"),
        ("YYZ", "LHR"),
        ("YYZ", "PVG"),
        ("YYZ", "HKG"),

        ("JFK", "YYZ"),
        ("JFK", "LAX"),
        ("JFK", "LHR"),
        ("JFK", "CDG"),

        ("LAX", "YYZ"),
        ("LAX", "JFK"),
        ("LAX", "NRT"),
        ("LAX", "HKG"),
        ("LAX", "SIN"),

        ("YVR", "YYZ"),
        ("YVR", "NRT"),
        ("YVR", "HKG"),

        ("LHR", "YYZ"),
        ("LHR", "JFK"),
        ("LHR", "CDG"),

        ("CDG", "LHR"),
        ("CDG", "JFK"),

        ("PVG", "YYZ"),
        ("PVG", "HKG"),
        ("PVG", "NRT"),
        ("PVG", "SIN"),

        ("HKG", "YYZ"),
        ("HKG", "PVG"),
        ("HKG", "NRT"),
        ("HKG", "SIN"),

        ("NRT", "LAX"),
        ("NRT", "YVR"),
        ("NRT", "HKG"),
        ("NRT", "SIN"),

        ("SIN", "HKG"),
        ("SIN", "NRT"),
        ("SIN", "PVG")
    ]

    flights = []

    start_date = datetime(2026, 10, 1)
    end_date = datetime(2027, 9, 30)

    total_days = (end_date - start_date).days

    # Create recurring Potter Airlines flight services
    flight_services = []

    for i in range(200):

        origin, destination = random.choice(routes)

        flight_service = {
            "flight_number": f"PA{100 + i}",
            "origin": origin,
            "destination": destination,
            "capacity": random.randint(150, 300),
            "base_fare": round(random.uniform(100, 800), 2)
        }

        flight_services.append(flight_service)

    # Generate scheduled flights
    for _ in range(number_of_flights):

        service = random.choice(flight_services)

        departure_date = start_date + timedelta(
            days=random.randint(0, total_days)
        )

        capacity = service["capacity"]

        # Most flights are between 20% and 95% occupied
        occupancy_rate = random.uniform(0.20, 0.95)

        seats_remaining = round(
            capacity * (1 - occupancy_rate)
        )

        assert seats_remaining <= capacity
        assert service["origin"] != service["destination"]

        flight = {
            "flight_number": service["flight_number"],
            "origin": service["origin"],
            "destination": service["destination"],
            "departure_date": departure_date.strftime("%Y-%m-%d"),
            "base_fare": service["base_fare"],
            "seats_remaining": seats_remaining,
            "capacity": capacity,
        }

        flights.append(flight)

    return flights


if not os.path.exists("data/flights_original.csv"):

    flights = generate_flights(10000)

    df = pd.DataFrame(flights)

    df = df.sort_values(
        ["departure_date", "flight_number"]
    )

    df.to_csv(
        "data/flights_original.csv",
        index=False
    )

    print("Original flight data created with 10,000 flights.")


if not os.path.exists("data/flights.csv"):

    original_df = pd.read_csv(
        "data/flights_original.csv"
    )

    original_df.to_csv(
        "data/flights.csv",
        index=False
    )

    print("Working flight data created.")