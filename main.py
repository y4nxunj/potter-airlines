import pandas as pd
from src.analysis import load_flights, filter_flights
from src.flight import Flight

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

# here we search for flights from loaded data from source
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
        # here we go through all matched flight in the filtered df one row at a time
        # and we take the columns and create actual flight object
        for _, row in filtered_df.iterrows():
            flight = Flight(
                row["flight_number"],
                row["origin"],
                row["destination"],
                row["departure_date"],
                row["seats_remaining"],
                row["capacity"],
                row["base_fare"],
            )

        print(f"\nFlight: {flight.flight_number}")
        print(f"Route: {flight.origin} -> {flight.destination}")
        print(f"Departure: {flight.departure_date.date()}")
        print(f"Seats remaining: {flight.seats_remaining}")
        print(f"Dynamic price: ${flight.get_price()}")


if __name__ == "__main__":
    search_flights()