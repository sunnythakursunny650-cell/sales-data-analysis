"""
Realistic Sales Dataset Generator
==================================
Generates a multi-year e-commerce sales transaction dataset with
realistic seasonality, pricing dynamics, regional distribution,
and controlled data anomalies for data cleaning demonstrations.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_sales_data(output_path="data/raw/sales_data.csv", num_rows=3600, random_state=42):
    """Generates a realistic retail/e-commerce sales dataset and saves it to CSV."""
    np.random.seed(random_state)
    random.seed(random_state)

    # 1. Geographic reference data
    geo_data = {
        "West": [
            ("California", "Los Angeles"),
            ("California", "San Francisco"),
            ("California", "San Diego"),
            ("Washington", "Seattle"),
            ("Oregon", "Portland"),
            ("Arizona", "Phoenix")
        ],
        "East": [
            ("New York", "New York City"),
            ("Pennsylvania", "Philadelphia"),
            ("Massachusetts", "Boston"),
            ("New Jersey", "Newark"),
            ("Maryland", "Baltimore")
        ],
        "Central": [
            ("Illinois", "Chicago"),
            ("Texas", "Houston"),
            ("Texas", "Dallas"),
            ("Texas", "Austin"),
            ("Michigan", "Detroit"),
            ("Ohio", "Columbus")
        ],
        "South": [
            ("Florida", "Miami"),
            ("Florida", "Orlando"),
            ("Georgia", "Atlanta"),
            ("North Carolina", "Charlotte"),
            ("Virginia", "Richmond")
        ]
    }

    # 2. Product Catalog & Cost Economics
    catalog = {
        "Technology": {
            "Laptops": (550.0, 1800.0, 0.72),        # (min_price, max_price, cost_ratio)
            "Smartphones": (300.0, 1100.0, 0.70),
            "Accessories": (25.0, 120.0, 0.50),
            "Printers": (150.0, 600.0, 0.78),
            "Copiers": (800.0, 2500.0, 0.65)
        },
        "Furniture": {
            "Chairs": (90.0, 450.0, 0.75),
            "Tables": (200.0, 950.0, 0.88),         # High cost, vulnerable to loss on discount
            "Bookcases": (120.0, 550.0, 0.80),
            "Furnishings": (20.0, 180.0, 0.58)
        },
        "Office Supplies": {
            "Storage": (30.0, 250.0, 0.62),
            "Binders": (5.0, 45.0, 0.45),
            "Paper": (8.0, 60.0, 0.48),
            "Art": (10.0, 85.0, 0.52),
            "Appliances": (60.0, 320.0, 0.74),
            "Envelopes": (5.0, 35.0, 0.42),
            "Fasteners": (3.0, 25.0, 0.40)
        }
    }

    # 3. Customer Pool
    first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
                   "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
                   "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                  "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]

    customer_pool = []
    for i in range(1, 351):
        c_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        c_id = f"CUST-{i:04d}"
        c_seg = random.choices(["Consumer", "Corporate", "Home Office"], weights=[0.53, 0.31, 0.16])[0]
        customer_pool.append((c_id, c_name, c_seg))

    # Shipping modes and payment methods
    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
    ship_weights = [0.60, 0.20, 0.14, 0.06]
    payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "Cash on Delivery"]
    payment_weights = [0.55, 0.25, 0.12, 0.08]

    # Date range: 2022-01-01 to 2024-12-31 (3 full years)
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    total_days = (end_date - start_date).days

    rows = []
    order_counter = 10001

    for _ in range(num_rows):
        order_id = f"ORD-{order_counter}"
        order_counter += 1

        # Realistic Seasonality: Higher sales in Q4 (months 10, 11, 12) & Spring (month 3)
        day_offset = random.randint(0, total_days)
        order_dt = start_date + timedelta(days=day_offset)
        month = order_dt.month
        # Re-roll slightly in low seasons to naturally create Q4 seasonal uplift
        if month in [10, 11, 12] or (month in [3, 6, 9] and random.random() < 0.3):
            pass
        elif random.random() < 0.15:
            # Shift some random orders into Q4
            order_dt = datetime(order_dt.year, random.choice([10, 11, 12]), random.randint(1, 28))

        # Shipping delay based on ship mode
        ship_mode = random.choices(ship_modes, weights=ship_weights)[0]
        if ship_mode == "Same Day":
            ship_dt = order_dt
        elif ship_mode == "First Class":
            ship_dt = order_dt + timedelta(days=random.randint(1, 2))
        elif ship_mode == "Second Class":
            ship_dt = order_dt + timedelta(days=random.randint(2, 4))
        else:
            ship_dt = order_dt + timedelta(days=random.randint(3, 7))

        # Customer selection
        cust = random.choice(customer_pool)
        cust_id, cust_name, cust_seg = cust

        # Geographic selection
        region = random.choices(["West", "East", "Central", "South"], weights=[0.32, 0.29, 0.22, 0.17])[0]
        state, city = random.choice(geo_data[region])

        # Category and Sub-category selection
        category = random.choices(["Technology", "Furniture", "Office Supplies"], weights=[0.36, 0.32, 0.32])[0]
        sub_category = random.choice(list(catalog[category].keys()))
        min_p, max_p, cost_ratio = catalog[category][sub_category]

        unit_price = round(random.uniform(min_p, max_p), 2)
        quantity = random.choices([1, 2, 3, 4, 5, 6, 7, 8], weights=[0.30, 0.26, 0.18, 0.12, 0.07, 0.04, 0.02, 0.01])[0]

        # Discount tiers (0%, 5%, 10%, 15%, 20%, 30%, 40%, 50%)
        discount = random.choices(
            [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50],
            weights=[0.42, 0.14, 0.16, 0.12, 0.08, 0.04, 0.02, 0.02]
        )[0]

        # Pricing math
        gross_sales = unit_price * quantity
        net_sales = round(gross_sales * (1.0 - discount), 2)
        unit_cost = round(unit_price * cost_ratio, 2)
        total_cost = round(unit_cost * quantity, 2)
        profit = round(net_sales - total_cost, 2)

        product_id = f"PROD-{category[:3].upper()}-{sub_category[:3].upper()}-{random.randint(100, 999)}"
        product_name = f"{sub_category} Model-{random.choice(['Alpha', 'Pro', 'Max', 'Elite', 'Standard', 'Plus'])} {random.randint(10, 99)}"
        payment_method = random.choices(payment_methods, weights=payment_weights)[0]

        rows.append({
            "Order_ID": order_id,
            "Order_Date": order_dt.strftime("%Y-%m-%d"),
            "Ship_Date": ship_dt.strftime("%Y-%m-%d"),
            "Ship_Mode": ship_mode,
            "Customer_ID": cust_id,
            "Customer_Name": cust_name,
            "Customer_Segment": cust_seg,
            "Country": "United States",
            "Region": region,
            "State": state,
            "City": city,
            "Product_ID": product_id,
            "Category": category,
            "Sub_Category": sub_category,
            "Product_Name": product_name,
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Discount": discount,
            "Sales": net_sales,
            "Profit": profit,
            "Payment_Method": payment_method
        })

    df = pd.DataFrame(rows)

    # 4. Inject Realistic Data Imperfections for Cleaning Demonstration
    # a) Controlled duplicates (12 rows)
    dup_indices = np.random.choice(df.index, size=12, replace=False)
    duplicates = df.loc[dup_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)

    # b) Minor missing values in non-critical columns (e.g. Payment_Method or slight whitespace in Category)
    null_indices = np.random.choice(df.index, size=20, replace=False)
    df.loc[null_indices, "Payment_Method"] = np.nan

    # c) Inconsistent whitespace in some text fields
    whitespace_indices = np.random.choice(df.index, size=25, replace=False)
    df.loc[whitespace_indices, "Category"] = df.loc[whitespace_indices, "Category"].apply(lambda x: f"  {x}  ")

    # Ensure parent directories exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[Data Generator] Successfully generated {len(df):,} rows with {df.shape[1]} columns at: {output_path}")
    return df

if __name__ == "__main__":
    generate_sales_data()
