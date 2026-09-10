"""
Main Automated Analytics Pipeline
=================================
Executes the end-to-end Data Analytics workflow:
1. Validates or generates the raw sales dataset.
2. Cleans dirty records, removes duplicates, and engineers features.
3. Computes executive KPIs, trend analyses, and margin metrics.
4. Generates and saves high-resolution portfolio visualizations.
5. Prints key business insights and dashboard launch instructions.

(Note: The original foundational NumPy proof-of-concept is preserved in `legacy_main_numpy.py`)
"""

import os
import sys

# Add src to system path for modular imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from data_generator import generate_sales_data
from data_cleaning import clean_sales_data
from analysis import (
    calculate_executive_kpis,
    analyze_monthly_trends,
    analyze_category_performance,
    analyze_regional_performance,
    analyze_discount_impact,
    analyze_customer_segments,
    get_top_bottom_products
)
from visualization import generate_all_visualizations

def run_pipeline():
    print("=" * 75)
    print("      ENTERPRISE SALES DATA ANALYTICS & BUSINESS INTELLIGENCE PIPELINE      ")
    print("=" * 75)

    raw_data_path = "data/raw/sales_data.csv"
    processed_data_path = "data/processed/sales_data_cleaned.csv"
    figures_dir = "reports/figures"

    # Step 1: Ensure dataset exists
    if not os.path.exists(raw_data_path):
        print(f"\n[Step 1] Raw dataset not found. Generating realistic sales dataset at '{raw_data_path}'...")
        generate_sales_data(output_path=raw_data_path)
    else:
        print(f"\n[Step 1] Found existing raw dataset at '{raw_data_path}'.")

    # Step 2: Data Cleaning & Preprocessing
    print("\n[Step 2] Executing data cleaning and feature engineering...")
    df = clean_sales_data(raw_csv_path=raw_data_path, processed_csv_path=processed_data_path, verbose=True)

    # Step 3: Executive KPIs
    print("\n[Step 3] Calculating Executive Business Metrics...")
    kpis = calculate_executive_kpis(df)
    print("-" * 55)
    print(f" {'EXECUTIVE KPI SUMMARY':^53}")
    print("-" * 55)
    for k, v in kpis.items():
        if "Sales" in k or "Profit" in k or "AOV" in k:
            print(f"  * {k:<35}: ${v:,.2f}")
        elif "%" in k:
            print(f"  * {k:<35}: {v:.2f}%")
        else:
            print(f"  * {k:<35}: {v:,}")
    print("-" * 55)

    # Step 4: Category & Regional Breakdowns
    print("\n[Step 4] Category Profitability Breakdown:")
    cat_df = analyze_category_performance(df)
    cat_summary = cat_df.groupby("Category").agg(
        Total_Sales=("Total_Sales", "sum"),
        Total_Profit=("Total_Profit", "sum")
    ).reset_index()
    cat_summary["Margin_%"] = (cat_summary["Total_Profit"] / cat_summary["Total_Sales"] * 100).round(2)
    for _, row in cat_summary.iterrows():
        print(f"  * {row['Category']:<16} | Sales: ${row['Total_Sales']:>10,.2f} | Profit: ${row['Total_Profit']:>9,.2f} | Margin: {row['Margin_%']:>5.1f}%")

    print("\n[Step 5] Regional Revenue Breakdown:")
    reg_df = analyze_regional_performance(df)
    for _, row in reg_df.iterrows():
        print(f"  * {row['Region']:<10} | Sales: ${row['Total_Sales']:>10,.2f} ({row['Sales_Share_%']:>5.1f}%) | Margin: {row['Profit_Margin_%']:>5.1f}%")

    # Step 5: Discount Impact
    print("\n[Step 6] Discount Sensitivity Analysis:")
    disc_df = analyze_discount_impact(df)
    for _, row in disc_df.iterrows():
        print(f"  * {row['Discount_Tier']:<18} | Sales: ${row['Total_Sales']:>10,.2f} | Margin: {row['Profit_Margin_%']:>5.1f}% | Loss Rate: {row['Loss_Rate_%']:>4.1f}%")

    # Step 6: Generate Visualizations
    print("\n[Step 7] Generating publication-quality charts for portfolio...")
    saved_paths = generate_all_visualizations(df, output_dir=figures_dir)

    print("\n" + "=" * 75)
    print(" PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 75)
    print(f" -> Processed data saved at : {processed_data_path}")
    print(f" -> Portfolio charts saved at: {figures_dir}/ ({len(saved_paths)} images)")
    print("\nTo launch the interactive Streamlit Web Dashboard, run:")
    print("    python -m streamlit run app.py")
    print("=" * 75)

if __name__ == "__main__":
    run_pipeline()
