"""

This file contains unit tests for the functions defined in 
src/analysis.py, which handle flight data analysis tasks such as 
filtering flights, calculating occupancy rates, and identifying the 
cheapest flights.

"""

import pandas as pd

from src.analysis import add_occupancy_rate, filter_flights, get_cheapest_flights

# create a small DataFrame used by the analysis tests
def make_test_data():
    """Create a small DataFrame used by the analysis tests."""
    return pd.DataFrame({
        "flight_number": ["PA100", "PA101", "PA102", "PA103"],
        "origin": ["YYZ", "YYZ", "YYZ", "PVG"],
        "destination": ["YVR", "YVR", "LAX", "YYZ"],
        "departure_date": pd.to_datetime([
            "2027-02-18", "2027-02-18", "2027-02-18", "2027-03-10"
        ]),
        "base_fare": [300, 200, 100, 400],
        "seats_remaining": [50, 0, 25, 80],
        "capacity": [100, 100, 100, 200]
    })

# Test filter_flights returns the correct flights based on 
# origin, destination, and departure date
def test_filter_flights():
    flights = make_test_data()

    selected = filter_flights(
        flights,
        "YYZ",
        "YVR",
        pd.to_datetime("2027-02-18")
    )

    assert len(selected) == 1
    assert selected.iloc[0]["flight_number"] == "PA100"

# Test filter_flights removes flights that are 
# sold out (seats_remaining = 0)
def test_filter_removes_sold_out_flights():
    flights = make_test_data()

    selected = filter_flights(
        flights,
        "YYZ",
        "YVR",
        pd.to_datetime("2027-02-18")
    )

    assert "PA101" not in selected["flight_number"].tolist()

# Test filter_flights returns an empty DataFrame when no flights 
# match the criteria
def test_filter_no_match():
    flights = make_test_data()

    selected = filter_flights(
        flights,
        "LHR",
        "CDG",
        pd.to_datetime("2027-02-18")
    )

    assert selected.empty

# Test add_occupancy_rate correctly calculates the occupancy rate for 
# each flight
def test_add_occupancy_rate():
    flights = make_test_data()
    result = add_occupancy_rate(flights)

    assert result.loc[0, "occupancy_rate"] == 0.5
    assert result.loc[1, "occupancy_rate"] == 1.0
    assert result.loc[2, "occupancy_rate"] == 0.75
    assert result.loc[3, "occupancy_rate"] == 0.6

# Test get_cheapest_flights returns correct flight_id and the price
def test_get_cheapest_flights():
    flights = make_test_data()
    cheapest = get_cheapest_flights(flights, 2)

    assert len(cheapest) == 2
    assert cheapest["flight_number"].tolist() == ["PA102", "PA101"]
    assert cheapest["base_fare"].tolist() == [100, 200]

# Run all analysis tests.
def run_analysis_tests():
    test_filter_flights()
    test_filter_removes_sold_out_flights()
    test_filter_no_match()
    test_add_occupancy_rate()
    test_get_cheapest_flights()
    print("All analysis tests passed.")


if __name__ == "__main__":
    run_analysis_tests()
