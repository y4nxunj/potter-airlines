import pandas as pd
# NOTE: I am adding this for efficient compatibility with analysis.py
from src.analysis import load_flights, filter_flights

# wirte a prompt to ask the use to write the origin and destination
# updating for airport code case sensitivity
def get_user_input():
    origin = input("Enter the origin airport code (e.g., YYZ): ").upper()

    destination = input("Enter the destination airport code (e.g., PVG): ").upper()
    
    departure_year = input("Enter the departure year (YYYY): ")
    departure_month = input("Enter the departure month (MM): ")
    departure_day = input("Enter the departure day (DD): ")
    departure_date_str = f"{departure_year}-{departure_month}-{departure_day}"
    
    # convert string to datetime object
    departure_date = pd.to_datetime(departure_date_str)
    
    return origin, destination, departure_date


def search_flights():
    flights_df = load_flights()

    origin, destination, departure_date = get_user_input()

    filtered_df = filter_flights(
        flights_df, origin, destination, departure_date
    )

    if filtered_df.empty:
        print("\nNo available flights found.")
    else:
        print("\nAvailable flights:")
        print(filtered_df)


if __name__ == "__main__":
    search_flights()