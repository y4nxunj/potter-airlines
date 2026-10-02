# Potter Airlines Dynamic Pricing System

## Overview

Potter Airlines is a Python-based airline management and dynamic pricing system.

The project simulates flight operations using 10,000 fictional scheduled flights. Users can search for available flights, compare dynamically calculated ticket prices, book seats, and view low-cost flight options.

The project demonstrates Python programming concepts including:

- Object-oriented programming
- Functions and modules
- Pandas DataFrames
- Vectorized calculations
- CSV file persistence
- Dynamic pricing
- User input and validation
- Automated testing

---

## Project Structure

```text
potter-airlines/
│
├── data/
│   ├── generate_flights.py
│   ├── flights_original.csv
│   └── flights.csv
│
├── src/
│   ├── analysis.py
│   ├── booking.py
│   └── flight.py
│
├── test/
│   ├── test_analysis.py
│   ├── test_flight.py
│   └── test_generate_flights.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Setup and Running the Program

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Run the main program from the project root directory:

```bash
python main.py
```

The program provides three options:

1. Search and book a flight
2. Show the cheapest flights
3. Exit the program

To run the automated tests:

```bash
python -m pytest
```

---

## Pricing Logic

The system calculates a dynamic ticket price for each flight using the following formula:

```text
Dynamic Price = Base Fare × Load Factor × Seasonal Factor × Time Factor
```

The **load factor** increases the price when fewer seats are available:

- More than 50% of seats remaining: 1.0
- Between 10% and 50% of seats remaining: 1.2
- 10% or fewer seats remaining: 1.5

The **seasonal factor** accounts for higher demand during certain months:

- June, July, and August: 1.3
- December and January: 1.5
- April: 1.2
- Other months: 1.0

The **time factor** increases the price when the departure date gets closer:

- Less than 7 days: 1.55
- Less than 21 days: 1.2
- Less than 60 days: 1.11
- 60 days or more: 1.0

The final ticket price is bounded between $100 and $2,000.

---

## Design Choices

The project generates 10,000 scheduled flights across 200 recurring flight services, with flight numbers ranging from PA100 to PA299.

A fixed random seed of 42 is used so that the generated flight data is reproducible.

The project uses two CSV files:

- `flights_original.csv` stores the original generated flight data and acts as a backup.
- `flights.csv` is the working dataset and is updated when customers successfully book seats.

Pandas is used to load and filter flight data, calculate occupancy rates, and sort and rank flight options.

The booking system calculates the dynamic price of each matching flight and displays the available flights from the cheapest to the most expensive.

---

## Testing and Validation

The project contains three test modules:

- `test_generate_flights.py` tests the generated flight data.
- `test_flight.py` tests the Flight class, seat updates, pricing factors, price boundaries, and invalid inputs.
- `test_analysis.py` tests flight filtering, occupancy-rate calculations, and cheapest-flight selection.

The program also handles important edge cases, including invalid dates, invalid booking quantities, insufficient remaining seats, past flights, and ticket prices outside the allowed range.

---

## Known Limitations

- The flight data is fictional and generated for demonstration purposes.
- The dynamic pricing factors are predefined rules rather than being estimated from real airline demand data.
- Flight information is stored using CSV files rather than a database.
- Flight schedules include departure dates but not specific departure times.
- The system does not include payment processing, authentication, or seat selection.

---

## LLM Statement

This project was developed with assistance from ChatGPT throughout the coding process. ChatGPT was used to assist with code development, generate realistic flight data, troubleshoot and fix coding errors, suggest test cases to improve test coverage, and help connect the workflow between different files and modules in the project.

All final code was reviewed, tested, and understood by the project team.