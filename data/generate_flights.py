import random
import pandas as pd
import os
from datetime import datetime, timedelta


# Makes the randomly generated data reproducible
random.seed(42)


def generate_flights(number_of_flights=100):

    airports = [
        "YYZ",  # Toronto
        "PVG",  # Shanghai
        "LAX",  # Los Angeles
        "JFK",  # New York
        "LHR",  # London
        "CDG",  # Paris
        "HKG",  # Hong Kong
        "NRT",  # Tokyo
        "YVR",  # Vancouver
        "SIN"   # Singapore
    ]

    flights = []

    # One full year of flight data
    start_date = datetime(2026, 10, 1)
    end_date = datetime(2027, 9, 30)

    total_days = (end_date - start_date).days

    for i in range(number_of_flights):

        # Flight number starts with PA followed by 3 digits
        flight_number = f"PA{100 + i}"

        # Choose two different airports
        origin, destination = random.sample(airports, 2)

        # Generate departure date within one year
        departure_date = start_date + timedelta(
            days=random.randint(0, total_days)
        )

        # Generate capacity between 100 and 300
        capacity = random.randint(100, 300)

        # Seats remaining cannot be greater than capacity
        seats_remaining = random.randint(0, capacity)

        # Generate base fare between $100 and $800
        base_fare = round(random.uniform(100, 800), 2)

        # Validation
        assert seats_remaining <= capacity
        assert origin != destination

        flight = {
            "flight_number": flight_number,
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date.strftime("%Y-%m-%d"),
            "base_fare": base_fare,
            "seats_remaining": seats_remaining,
            "capacity": capacity,
        }

        flights.append(flight)

    return flights


# Create original dataset only once
if not os.path.exists("data/flights_original.csv"):

    flights = generate_flights(100)

    df = pd.DataFrame(flights)

    df.to_csv("data/flights_original.csv", index=False)

    print("Original flight data created.")


# Create working copy only if it does not already exist
if not os.path.exists("data/flights.csv"):

    original_df = pd.read_csv("data/flights_original.csv")

    original_df.to_csv("data/flights.csv", index=False)

    print("Working flight data created.")