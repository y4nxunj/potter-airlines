"""Tests for the current src/flight.py file."""

import datetime

from src.flight import Flight


def check_assertion(function):
    """Confirm that invalid input causes an AssertionError."""
    try:
        function()
        assert False, "Expected an AssertionError"
    except AssertionError:
        pass


def test_flight_validation():
    departure = datetime.datetime.today() + datetime.timedelta(days=100)

    check_assertion(
        lambda: Flight("PA100", "YYZ", "YVR", departure, 0, 0, 200)
    )
    check_assertion(
        lambda: Flight("PA100", "YYZ", "YVR", departure, -1, 100, 200)
    )
    check_assertion(
        lambda: Flight("PA100", "YYZ", "YVR", departure, 101, 100, 200)
    )


def test_has_capacity():
    departure = datetime.datetime.today() + datetime.timedelta(days=100)
    available = Flight("PA100", "YYZ", "YVR", departure, 10, 100, 200)
    sold_out = Flight("PA101", "YYZ", "YVR", departure, 0, 100, 200)

    assert available.has_capacity() is True
    assert sold_out.has_capacity() is False


def test_update_seats_remaining():
    departure = datetime.datetime.today() + datetime.timedelta(days=100)
    flight = Flight("PA100", "YYZ", "YVR", departure, 10, 100, 200)

    assert flight.update_seats_remaining(0) is False
    assert flight.update_seats_remaining(-1) is False
    assert flight.update_seats_remaining(11) is False
    assert flight.seats_remaining == 10

    assert flight.update_seats_remaining(4) is True
    assert flight.seats_remaining == 6


def test_load_factor_boundaries():
    departure = datetime.datetime.today() + datetime.timedelta(days=100)

    above_half = Flight("PA100", "YYZ", "YVR", departure, 51, 100, 200)
    exactly_half = Flight("PA101", "YYZ", "YVR", departure, 50, 100, 200)
    above_ten = Flight("PA102", "YYZ", "YVR", departure, 11, 100, 200)
    exactly_ten = Flight("PA103", "YYZ", "YVR", departure, 10, 100, 200)

    assert above_half.get_load_factor() == 1.0
    assert exactly_half.get_load_factor() == 1.2
    assert above_ten.get_load_factor() == 1.2
    assert exactly_ten.get_load_factor() == 1.5


def test_seasonal_factors():
    def make_flight(month):
        departure = datetime.datetime(2027, month, 15)
        return Flight("PA100", "YYZ", "YVR", departure, 50, 100, 200)

    assert make_flight(7).get_seasonal_factor() == 1.3
    assert make_flight(12).get_seasonal_factor() == 1.5
    assert make_flight(4).get_seasonal_factor() == 1.2
    assert make_flight(3).get_seasonal_factor() == 1.0


def test_time_factors():
    now = datetime.datetime.today()

    five_days = Flight("PA100", "YYZ", "YVR",
                       now + datetime.timedelta(days=5), 50, 100, 200)
    ten_days = Flight("PA101", "YYZ", "YVR",
                      now + datetime.timedelta(days=10), 50, 100, 200)
    thirty_days = Flight("PA102", "YYZ", "YVR",
                         now + datetime.timedelta(days=30), 50, 100, 200)
    ninety_days = Flight("PA103", "YYZ", "YVR",
                         now + datetime.timedelta(days=90), 50, 100, 200)

    assert five_days.get_time_factor() == 1.55
    assert ten_days.get_time_factor() == 1.2
    assert thirty_days.get_time_factor() == 1.11
    assert ninety_days.get_time_factor() == 1.0


def test_past_flight():
    departure = datetime.datetime.today() - datetime.timedelta(days=2)
    flight = Flight("PA100", "YYZ", "YVR", departure, 50, 100, 200)

    try:
        flight.get_time_factor()
        assert False, "A departed flight should raise ValueError"
    except ValueError:
        pass


def test_price_equation():
    departure = datetime.datetime.today() + datetime.timedelta(days=100)
    flight = Flight("PA100", "YYZ", "YVR", departure, 50, 100, 200)

    expected_price = round(
        flight.base_fare
        * flight.get_load_factor()
        * flight.get_seasonal_factor()
        * flight.get_time_factor(),
        2
    )
    assert flight.get_price() == expected_price


def run_flight_tests():
    test_flight_validation()
    test_has_capacity()
    test_update_seats_remaining()
    test_load_factor_boundaries()
    test_seasonal_factors()
    test_time_factors()
    test_past_flight()
    test_price_equation()
    print("All Flight tests passed.")


if __name__ == "__main__":
    run_flight_tests()
