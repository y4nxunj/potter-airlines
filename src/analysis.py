"""
analysis.py - summary of flight data for Potter Airlines

This file contains functions to filter and analyze flight data.
It produces summaries of flight data, such as the cheapest flights, and can be used to support the booking process.

"""

import pandas as pd

# we load the data file and need date and time into string
def load_flights():
    flights_df = pd.read_csv(
        "data/flights.csv",
        parse_dates=["departure_date"]
    )
    return flights_df


# filter the same origin and destination
# asking the user to put the year first, then month, then day to get the departure date
# added seats remaining to be non zero

def filter_flights(flights_df, origin, destination, departure_date):
    filtered_df = flights_df[
        (flights_df['origin'] == origin) &
        (flights_df['destination'] == destination) &
        (flights_df['departure_date'] == departure_date) &
        (flights_df["seats_remaining"] > 0)
    ]
    return filtered_df

# this is the rate of how much seats taken
def add_occupancy_rate(flights_df):
    flights_df["occupancy_rate"] = (
        1 - flights_df["seats_remaining"]/flights_df["capacity"]
    )
    return flights_df


# this gets cheapest flight by base fare, not the final dynamic pricing
def get_cheapest_flights(flights_df, number_of_flights=5):
    cheapest_flights = flights_df.sort_values(
        "base_fare"
    ).drop_duplicates(subset="flight_number").head(number_of_flights)

    return cheapest_flights
