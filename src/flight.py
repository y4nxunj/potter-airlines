from datetime import date, datetime


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

    def has_capacity(self):
        return self.seats_remaining > 0

    def update_seats_remaining(self, booked_seats):
        self.seats_remaining -= booked_seats

    def get_load_factor(self):
        return self.seats_remaining / self.capacity

    def get_seasonal_factor(self):
        departure_date = self.departure_date
        if isinstance(departure_date, str):
            departure_date = date.fromisoformat(departure_date)
        elif isinstance(departure_date, datetime):
            departure_date = departure_date.date()

        if departure_date.month == 12 and departure_date.day == 25:
            return 1.5

        year = departure_date.year
        a = year % 19
        b, c = divmod(year, 100)
        d, e = divmod(b, 4)
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i, k = divmod(c, 4)
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        easter = date(year, (h + l - 7 * m + 114) // 31,
                      (h + l - 7 * m + 114) % 31 + 1)
        if departure_date == easter:
            return 1.2

        if ((departure_date.month == 10 and departure_date.weekday() == 0
             and 8 <= departure_date.day <= 14)
                or (departure_date.month == 11 and departure_date.weekday() == 3
                    and 22 <= departure_date.day <= 28)):
            return 1.2

        if departure_date.month in (1, 6, 7, 8, 12):
            return 1.2
        return 1.0

    def get_time_factor(self):

        if self.departure_date <7:
            return 1.5
        elif self.departure_date < 14:
            return 1.2
        else:
            return 1.0
