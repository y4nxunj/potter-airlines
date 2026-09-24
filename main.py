
# wirte a prompt to ask the use to write the origin and destination
def get_user_input():
    origin = input("Enter the origin airport code (e.g., LAX): ")
    destination = input("Enter the destination airport code (e.g., JFK): ")
    departure_year = input("Enter the departure year (YYYY): ")
    departure_month = input("Enter the departure month (MM): ")
    departure_day = input("Enter the departure day (DD): ")
    departure_date_str = f"{departure_year}-{departure_month}-{departure_day}"
    
    # Convert the string to a datetime object
    departure_date = pd.to_datetime(departure_date_str)
    
    return origin, destination, departure_date

