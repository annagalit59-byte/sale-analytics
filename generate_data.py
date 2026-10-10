import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

num_rows = 1_000_000
print(f"Generating {num_rows} simulated orders...")

categories = ['Electronics', 'Fashion', 'Home & Living', 'Beauty', 'Groceries', 'Sports', 'Toys', 'Books']
payment_methods = ['COD', 'GCash', 'Maya', 'Card']
regions = ['NCR', 'CALABARZON', 'Central Luzon', 'Central Visayas', 'Davao Region', 'Others']
region_weights = [0.40, 0.20, 0.15, 0.10, 0.10, 0.05]

base_date = datetime(2026, 11, 11)
hours = []
for _ in range(num_rows):
    r = random.random()
    if r < 0.25:
        h = 0
        m = random.randint(0, 59)
    elif r < 0.65:
        h = random.randint(20, 21)
        m = random.randint(0, 59)
    else:
        h = random.choice([x for x in range(24) if x != 0 and x not in [20, 21]])
        m = random.randint(0, 59)
    hours.append(base_date + timedelta(hours=h, minutes=m, seconds=random.randint(0, 59)))

data = {
    'order_id': [f"ORD-{i:07d}" for i in range(num_rows)],
    'timestamp': hours,
    'region': np.random.choice(regions, size=num_rows, p=region_weights),
    'category': np.random.choice(categories, size=num_rows),
    'unit_price': np.random.uniform(100, 15000, size=num_rows),
    'quantity': np.random.choice([1, 2, 3, 4, 5, -1, -2], size=num_rows, p=[0.7, 0.15, 0.05, 0.03, 0.02, 0.03, 0.02]),
    'payment_method': np.random.choice(payment_methods, size=num_rows, p=[0.5, 0.25, 0.15, 0.10]),
    'status': np.random.choice(['Delivered', 'Cancelled', 'Returned'], size=num_rows, p=[0.75, 0.15, 0.10])
}

df = pd.DataFrame(data)
df.loc[df.sample(frac=0.02).index, 'region'] = None
dups = df.sample(frac=0.01)
df = pd.concat([df, dups], ignore_index=True)
df['region'] = df['region'].apply(lambda x: x.lower() if pd.notnull(x) and random.random() < 0.1 else x)

# Save Parquet first while unit_price is purely numeric
os.makedirs('data', exist_ok=True)
parquet_path = 'data/orders.parquet'
df.to_parquet(parquet_path, index=False)

# Inject text prices for CSV
df['unit_price'] = df['unit_price'].apply(lambda x: f"₱{x:,.2f}" if random.random() < 0.05 else x)

csv_path = 'data/orders.csv'
df.to_csv(csv_path, index=False)

print(f"CSV Size: {os.path.getsize(csv_path) / (1024*1024):.2f} MB")
print(f"Parquet Size: {os.path.getsize(parquet_path) / (1024*1024):.2f} MB")
