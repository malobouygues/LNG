import pandas as pd

def calculate_freight_cost(charter_rate, travel_days, port_fees, cargo_size):
    return (charter_rate * travel_days + port_fees) / cargo_size

def calculate_boil_off(cargo_size, boil_off_rate, travel_days, destination_price):
    return (cargo_size * boil_off_rate * travel_days) * destination_price / cargo_size

def calculate_netback(destination_price, freight_cost, boil_off, regas_fees):
    return destination_price - freight_cost - boil_off - regas_fees
