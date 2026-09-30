import pandas as pd
from src.analysis import load_flights, filter_flights, get_cheapest_flights
from src.flight import Flight

# wirte a prompt to ask the use to write the origin and destination
# updating for airport code case sensitivity
def get_user_input():
    origin = input("Enter the origin airport code (e.g., YYZ): ").upper()
    destination = input("Enter the destination airport code (e.g., PVG): ").upper()

    while True:
        try:
            departure_year = input("Enter the departure year (YYYY): ")
            departure_month = input("Enter the departure month (MM): ")
            departure_day = input("Enter the departure day (DD): ")
            departure_date_str = f"{departure_year}-{departure_month}-{departure_day}"
    
            # convert string to datetime object
            departure_date = pd.to_datetime(departure_date_str, format="%Y-%m-%d")
            break

        except ValueError:
            print("\nInvalid date. Please try again.\n")
    
    return origin, destination, departure_date


# this is used for booking seats in flight
def book_flights(flights_df, flight):
    while True:
        try:
            booked_seats = int(input("\nHow many seats would you like to book? "))

            if booked_seats <= 0:
                print("Please enter a number greater than 0.")
                continue

            if booked_seats > flight.seats_remaining:
                print(
                    f"Only {flight.seats_remaining} seats are available. "
                    "Please try again."
                )
                continue
            break


        except ValueError:
            print("Please enter a valid number.")

    if flight.update_seats_remaining(booked_seats):
        # this finds the corresponding flight in the df and updates its seats remaining
        flights_df.loc[
            (flights_df["flight_number"] == flight.flight_number) &
            (flights_df["departure_date"] == flight.departure_date), 
            "seats_remaining"] = flight.seats_remaining

        flights_df.to_csv(
            "data/flights.csv",
            index=False,
            date_format="%Y-%m-%d"
        )

        print("Booking successful!")
        print(f"Seats remaining: {flight.seats_remaining}")

    else:
        print("Booking failed. Please check the number of seats.")



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

        while True:
            # user select the flight they want to book
            selected_flight_number = input(
                "\nEnter the flight number you would like to book: "
            ).upper()

            selected_row = filtered_df[
                filtered_df["flight_number"] == selected_flight_number
            ]

            if selected_row.empty:
                print("Invalid flight number.")
            else:
                break

        row = selected_row.iloc[0]

        selected_flight = Flight(
            row["flight_number"],
            row["origin"],
            row["destination"],
            row["departure_date"],
            row["seats_remaining"],
            row["capacity"],
            row["base_fare"]
        )

        book_flights(flights_df, selected_flight)


# show cheapest flights calling exsiting sorting from analysis.py
def show_cheapest_flights():
    flights_df = load_flights()

    cheapest_flights = get_cheapest_flights(flights_df)

    print("\n5 Cheapest Flights by Base Fare:")

    for _, row in cheapest_flights.iterrows():
        print(
            f"{row['flight_number']}: "
            f"{row['origin']} -> {row['destination']} | "
            f"{row['departure_date'].date()} | "
            f"${row['base_fare']:.2f}"
        )


# add a main function to print messages
# and give user choices of prompt
def main():
    while True:
        print("\nWelcome to Potter Airlines!")
        print("1. Search and book a flight")
        print("2. Show cheapest flights")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            search_flights()

        elif choice == "2":
            show_cheapest_flights()

        elif choice == "3":
            print("Thank you for using Potter Airlines :)")
            break

        else:
            print("Invalid choice. Please try again")


if __name__ == "__main__":
    main()