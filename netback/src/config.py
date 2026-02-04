import os

script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cargo specifications
CARGO_SIZE = 3.5  # MMT (Million Metric Tons)

# Travel days
TRAVEL_DAYS_ASIA = 25
TRAVEL_DAYS_EUROPE = 10

# Boil-off rate (per day)
BOIL_OFF_RATE = 0.0015

# Fees
PORT_FEES = 500000  # USD
REGAS_FEES_ASIA = 0.5  # USD/MMBtu
REGAS_FEES_EUROPE = 0.4  # USD/MMBtu
