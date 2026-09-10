"""
Data Cleaning & Preprocessing Pipeline
======================================
Loads raw sales data, performs quality audits, cleans dirty/missing values,
eliminates duplicate entries, and engineers analytical features.
"""

import os
import pandas as pd
import numpy as np

def clean_sales_data(raw_csv_path="data/raw/sales_data.csv",
                     processed_csv_path="data/processed/sales_data_cleaned.csv",
                     verbose=True):
    """
    Cleans raw sales transaction data and generates derived analytical features.
    
    Steps:
    1. Ingest raw CSV data.
    2. Audit missing values and impute/standardize.
    3. Audit and drop duplicate rows.
    4. Strip extraneous whitespace from categorical text columns.
    5. Convert date columns into standard datetime objects.
    6. Validate numeric integrity (Sales, Profit, Quantity, Discount).
    7. Engineer time, margin, and segmentation features:
       - Shipping_Days: Days elapsed between order and shipment
       - Order_Year, Order_Month, Order_Month_Name, Year_Month, Quarter
       - Profit_Margin: Net profit percentage of sales
       - Discount_Tier: Categorized discount intensity
    8. Export cleaned dataset to processed directory.
    """
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw data file not found at: {raw_csv_path}")

    df = pd.read_csv(raw_csv_path)
    initial_rows = len(df)

    if verbose:
        print("=" * 60)
        print(" [DATA CLEANING PIPELINE STARTED]")
        print("=" * 60)
        print(f"Loaded raw dataset with {initial_rows:,} rows and {df.shape[1]} columns.")

    # 1. Audit and drop duplicate records
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        if verbose:
            print(f" -> Found & removed {dup_count} duplicate rows. Remaining: {len(df):,}")
    else:
        if verbose:
            print(" -> No duplicate rows detected.")

    # 2. Audit missing values
    null_counts = df.isnull().sum()
    columns_with_nulls = null_counts[null_counts > 0]
    if not columns_with_nulls.empty:
        if verbose:
            print(f" -> Columns with missing values:\n{columns_with_nulls}")
        if "Payment_Method" in df.columns:
            df["Payment_Method"] = df["Payment_Method"].fillna("Not Specified")
        df = df.dropna(subset=["Sales", "Profit", "Order_Date"]).reset_index(drop=True)
    else:
        if verbose:
            print(" -> No missing values found in critical columns.")

    # 3. Clean string columns (strip whitespace, standardize casing)
    string_cols = ["Category", "Sub_Category", "Customer_Segment", "Region", "Ship_Mode", "Payment_Method"]
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 4. Date parsing
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])

    # 5. Feature Engineering
    # Shipping Lead Time
    df["Shipping_Days"] = (df["Ship_Date"] - df["Order_Date"]).dt.days
    df["Shipping_Days"] = df["Shipping_Days"].clip(lower=0)

    # Time Features
    df["Order_Year"] = df["Order_Date"].dt.year
    df["Order_Month"] = df["Order_Date"].dt.month
    df["Order_Month_Name"] = df["Order_Date"].dt.strftime("%B")
    df["Year_Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Quarter"] = "Q" + df["Order_Date"].dt.quarter.astype(str)
    df["Year_Quarter"] = df["Order_Year"].astype(str) + "-" + df["Quarter"]

    # Financial & Margin Features
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce").round(2)
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce").round(2)
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce").round(2)
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce").round(4)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").astype(int)

    # Profit Margin Percentage
    # Safe division avoiding zero division
    df["Profit_Margin"] = np.where(
        df["Sales"] > 0,
        (df["Profit"] / df["Sales"] * 100).round(2),
        0.0
    )

    # Discount Tier Categorization
    def categorize_discount(disc):
        if disc == 0.0:
            return "No Discount (0%)"
        elif disc <= 0.10:
            return "Low (1-10%)"
        elif disc <= 0.20:
            return "Medium (11-20%)"
        else:
            return "High (>20%)"

    df["Discount_Tier"] = df["Discount"].apply(categorize_discount)

    # Profitability Status
    df["Is_Profitable"] = df["Profit"] > 0

    # Ensure output directory exists
    os.makedirs(os.path.dirname(processed_csv_path), exist_ok=True)
    df.to_csv(processed_csv_path, index=False)

    if verbose:
        print(f" -> Successfully saved cleaned dataset ({len(df):,} rows, {df.shape[1]} columns) to: {processed_csv_path}")
        print("=" * 60)

    return df

if __name__ == "__main__":
    clean_sales_data()
