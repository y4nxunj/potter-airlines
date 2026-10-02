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

        assert capacity > 0
        assert 0 <= seats_remaining <= capacity

        self.seats_remaining = seats_remaining
        self.capacity = capacity
        self.base_fare = base_fare


    def update_seats_remaining(self, booked_seats):

        # returns True if booking successful, 
        # false otherwise
        # update seats remaining after a booking if successful

        if booked_seats <= 0:
            return False
        if booked_seats > self.seats_remaining:
            return False
        
        self.seats_remaining -= booked_seats
        return True


    def get_load_factor(self):

        # returns a larger load factor for flights that are more full

        remain_percentage = self.seats_remaining / self.capacity

        if remain_percentage > 0.5:
            return 1.0
        elif remain_percentage > 0.1:
            return 1.2
        else:
            return 1.5


    def get_seasonal_factor(self):

        # demand is higher in summer and winter
        # maybe april
        # returns seasonal factor > 1.0 for these months and no change for other months

        month = self.departure_date.month

        if month in [6, 7, 8]:
            return 1.3
        elif month in [12, 1]: 
            return 1.5
        elif month in [4]:
            return 1.2
        
        return 1.0


    def get_time_factor(self):

        # returns a higher factor for flights that are closer to departure date

        days_until_departure = (self.departure_date - datetime.datetime.today().date()).days

        # added this error raise to preserve logic
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

        # calculate the dynamic price of the flight based on base fare, load factor, seasonal factor, and time factor

        price = (
            self.base_fare 
            * self.get_load_factor() 
            * self.get_seasonal_factor() 
            * self.get_time_factor()
        )

        minimum_price = 100
        maximum_price = 2000

        price = max(minimum_price, min(price, maximum_price))

        return round(price, 2)
    