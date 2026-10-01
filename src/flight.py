"""
flight.py - Flight class for Potter Airlines

Each flight has a flight number, origin, destination, departure date, seats remaining, capacity, and base fare.
The class also has methods to calculate the dynamic price of the flight based on load factor, seasonal factor, and time factor.
Other methods are included to validate and update the flight's capacity and seats remaining during the booking process.

"""

import datetime

class Flight:
    def __init__(self, flight_number, origin, destination, departure_date, seats_remaining, capacity, base_fare):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date

        # seats_remaining should be between 0 and capacity; capacity should be positive
        assert capacity > 0
        assert 0 <= seats_remaining <= capacity
        self.seats_remaining = seats_remaining
        self.capacity = capacity

        self.base_fare = base_fare

    # NOTE: not used
    def has_capacity(self):
        return self.seats_remaining > 0


    def update_seats_remaining(self, booked_seats):

        # Returns True if the booking was successful, 
        #         False otherwise (e.g., invalid number of seats or not enough seats remaining)
        # Update seats remaining after a booking if successful

        if booked_seats <= 0:
            return False
        if booked_seats > self.seats_remaining:
            return False
        
        self.seats_remaining -= booked_seats
        return True


    def get_load_factor(self):

        # Returns a larger load factor for flights that are more full

        remain_percentage = self.seats_remaining / self.capacity

        if remain_percentage > 0.5:
            return 1.0
        elif remain_percentage > 0.1:
            return 1.2
        else:
            return 1.5


    def get_seasonal_factor(self):

        # Demand is higher in summer (June, July, August) and winter (December, January)
        # maybe April
        # Returns a seasonal factor > 1.0 for these months, and no adjustments for other months

        month = self.departure_date.month

        if month in [6, 7, 8]:
            return 1.3
        elif month in [12, 1]: 
            return 1.5
        elif month in [4]:
            return 1.2
        
        return 1.0


    def get_time_factor(self):

        # Returns a higher factor for flights that are closer to departure date

        days_until_departure = (self.departure_date - datetime.datetime.today()).days

        # Added this error raise to preserve logic
        if days_until_departure < 0:
            raise ValueError("Flight has already departed.")
        
        if days_until_departure < 7:
            return 1.55
        elif days_until_departure < 21:
            return 1.2
        elif days_until_departure < 60:
            return 1.11
        else:
            return 1.0


    def get_price(self):

        # Calculate the dynamic price of the flight based on base fare, load factor, seasonal factor, and time factor

        price = (
            self.base_fare 
            * self.get_load_factor() 
            * self.get_seasonal_factor() 
            * self.get_time_factor()
        )

        return round(price, 2)
    