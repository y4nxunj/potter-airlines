from src.analysis import get_cheapest_flights, load_flights
from src.booking import search_flights


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
            f"From ${row['base_fare']:.2f}"
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