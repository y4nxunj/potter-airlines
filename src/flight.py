class Flight:
    def __init__(self, flight_number, origin, destination, departure_date, seats_remaining, capacity, base_fare):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date

        # seats_remaining should be between 0 and capacity
        assert 0 <= seats_remaining <= capacity
        self.seats_remaining = seats_remaining
        self.capacity = capacity

        self.base_fare = base_fare

    def has_capacity(self, requested_seats):
        return self.seats_remaining >= 0

    def update_seats_remaining(self, booked_seats):
        self.seats_remaining -= booked_seats

    def get_load_factor(self):
        # TODO
        return

    def get_seasonal_factor(self):

        # TODO
        # Demand is higher in summer (June, July, August) and winter (December, January)
        # maybe April
        # Holidays (e.g. Christmas - 1.5, Thanksgiving - 1.2, Easter - 1.2)

        return 1.0