import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Settings
rows = 10000
start_date = datetime(2024, 1, 1)

# Generate dummy data
dates = [start_date + timedelta(minutes=i) for i in range(rows)]
close_prices = np.random.normal(loc=40000, scale=500, size=rows) # Random prices around 40k

# Create DataFrame
data = {
    'timestamp': dates,
    'open': close_prices + np.random.normal(0, 50, rows),
    'high': close_prices + np.random.normal(50, 20, rows),
    'low': close_prices - np.random.normal(50, 20, rows),
    'close': close_prices, # The strictly required column
    'volume_btc': np.random.uniform(1, 10, rows),
    'volume_usd': np.random.uniform(40000, 400000, rows)
}

df = pd.DataFrame(data)

# Save to CSV
df.to_csv('data.csv', index=False)
print("✅ Successfully created data.csv with 10,000 rows!")