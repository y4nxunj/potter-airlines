import pandas as pd

# filter the same origin and destination
# asking the user to put the year first, then month, then day to get the departure date
# 
def filter_flights(flights_df, flight):
    filtered_df = flights_df[
        (flights_df['origin'] == flight.origin) &
        (flights_df['destination'] == flight.destination) &
        (flights_df['departure_date'] == flight.departure_date)
    ]
    return filtered_df


