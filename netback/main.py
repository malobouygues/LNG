import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

import src.config as config
from src.netback_formulas import calculate_freight_cost, calculate_boil_off, calculate_netback

start_date = datetime.now()
dates = pd.date_range(start=start_date, periods=24, freq='M')
df_market = pd.DataFrame(index=dates)

np.random.seed(42)
df_market['JKM_USD'] = np.random.uniform(12, 15, len(dates))
df_market['TTF_USD'] = np.random.uniform(10, 12, len(dates))
df_market['Charter_Rate'] = np.random.uniform(80000, 120000, len(dates))

# Calculate freight costs for both routes
# Freight cost = (Charter Rate * Travel Days + Port Fees) / Cargo Size
freight_cost_jkm = calculate_freight_cost(
    df_market['Charter_Rate'], 
    config.TRAVEL_DAYS_ASIA, 
    config.PORT_FEES, 
    config.CARGO_SIZE
)

freight_cost_ttf = calculate_freight_cost(
    df_market['Charter_Rate'], 
    config.TRAVEL_DAYS_EUROPE, 
    config.PORT_FEES, 
    config.CARGO_SIZE
)

boil_off_jkm = calculate_boil_off(
    config.CARGO_SIZE, 
    config.BOIL_OFF_RATE, 
    config.TRAVEL_DAYS_ASIA, 
    df_market['JKM_USD']
)

boil_off_ttf = calculate_boil_off(
    config.CARGO_SIZE, 
    config.BOIL_OFF_RATE, 
    config.TRAVEL_DAYS_EUROPE, 
    df_market['TTF_USD']
)

# Calculate netback prices for both destinations
# Netback = Destination Price - Freight Cost - Boil-off Loss - Regas Fees
# Netback represents the effective price received at origin after all costs
df_netback_jkm = calculate_netback(
    df_market['JKM_USD'], 
    freight_cost_jkm, 
    boil_off_jkm, 
    config.REGAS_FEES_ASIA
)

df_netback_ttf = calculate_netback(
    df_market['TTF_USD'], 
    freight_cost_ttf, 
    boil_off_ttf, 
    config.REGAS_FEES_EUROPE
)

# Calculate arbitrage spread between Asia and Europe
# Spread = Netback Asia - Netback Europe
# If spread > 0, cargo flows to Asia (JKM netback higher than TTF)
# If spread < 0, cargo flows to Europe (TTF netback higher than JKM)
# Spread represents the arbitrage opportunity between Asia and Europe markets
df_spread_arb = df_netback_jkm - df_netback_ttf

df_result = pd.DataFrame(index=dates)
df_result['netback_jkm'] = df_netback_jkm
df_result['netback_ttf'] = df_netback_ttf

if df_result is None or len(df_result) == 0:
    print("No data available")
else:
    plt.figure(figsize=(12, 6))
    
    plt.plot(df_result.index, df_result['netback_jkm'], 
             label='Netback JKM (Asia)', color='red', linewidth=2)
    
    plt.plot(df_result.index, df_result['netback_ttf'], 
             label='Netback TTF (Europe)', color='gray', linewidth=2)
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    plt.xticks(rotation=0)
    plt.legend()
    plt.title('LNG Netback Prices: Asia vs Europe', 
             fontsize=12, fontweight='bold')
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Netback Price ($/MMBtu)', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
