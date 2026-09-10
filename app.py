"""
Executive Sales & Profit Analytics Dashboard
============================================
An interactive Streamlit web application providing real-time KPI tracking,
interactive filtering, category diagnostics, discount sensitivity, and data export.

Run via:
    streamlit run app.py
or:
    python -m streamlit run app.py
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Add src to system path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
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

# Page configuration
st.set_page_config(
    page_title="Sales & Profit Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border-left: 5px solid #2b5c8f;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 6px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_prepare_data():
    processed_path = "data/processed/sales_data_cleaned.csv"
    raw_path = "data/raw/sales_data.csv"
    if os.path.exists(processed_path):
        df = pd.read_csv(processed_path)
    elif os.path.exists(raw_path):
        df = clean_sales_data(raw_path, processed_path, verbose=False)
    else:
        from data_generator import generate_sales_data
        generate_sales_data(raw_path)
        df = clean_sales_data(raw_path, processed_path, verbose=False)
    
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])
    return df

try:
    df_raw = load_and_prepare_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ----------------- SIDEBAR FILTERS ----------------- #
st.sidebar.title("🔍 Filter Controls")

min_date = df_raw["Order_Date"].min().date()
max_date = df_raw["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Region filter
all_regions = sorted(df_raw["Region"].unique().tolist())
selected_regions = st.sidebar.multiselect(
    "Region",
    options=all_regions,
    default=all_regions
)

# Category filter
all_categories = sorted(df_raw["Category"].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Category",
    options=all_categories,
    default=all_categories
)

# Customer Segment filter
all_segments = sorted(df_raw["Customer_Segment"].unique().tolist())
selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    options=all_segments,
    default=all_segments
)

# Filter dataframe
if len(date_range) == 2:
    start_dt, end_dt = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = df_raw[
        (df_raw["Order_Date"] >= start_dt) &
        (df_raw["Order_Date"] <= end_dt) &
        (df_raw["Region"].isin(selected_regions)) &
        (df_raw["Category"].isin(selected_categories)) &
        (df_raw["Customer_Segment"].isin(selected_segments))
    ]
else:
    filtered_df = df_raw

if filtered_df.empty:
    st.warning("No records match the selected filter criteria. Please broaden your selection.")
    st.stop()

# ----------------- DASHBOARD HEADER & KPIS ----------------- #
st.title("📈 Executive Sales & Profit Intelligence Dashboard")
st.caption(f"Analyzing {len(filtered_df):,} transactions across {filtered_df['Order_Year'].nunique()} operating years")

kpis = calculate_executive_kpis(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Revenue", f"${kpis['Total Sales']:,.2f}")
with col2:
    st.metric("Total Profit", f"${kpis['Total Profit']:,.2f}")
with col3:
    st.metric("Profit Margin", f"{kpis['Profit Margin %']:.1f}%")
with col4:
    st.metric("Total Orders", f"{kpis['Total Orders']:,}")
with col5:
    st.metric("Avg Order Value (AOV)", f"${kpis['Average Order Value (AOV)']:,.2f}")

st.markdown("---")

# ----------------- TABS NAVIGATION ----------------- #
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Trend Analysis",
    "📦 Category & Products",
    "🗺️ Regional Performance",
    "🏷️ Pricing & Discounts",
    "📋 Data Explorer"
])

# ----- TAB 1: Trend Analysis ----- #
with tab1:
    st.subheader("Monthly Revenue and Profit Growth")
    monthly = analyze_monthly_trends(filtered_df)
    
    fig, ax1 = plt.subplots(figsize=(10, 4))
    x = range(len(monthly))
    ax1.plot(x, monthly["Total_Sales"], marker="o", color="#1f77b4", linewidth=2, label="Sales ($)")
    ax1.plot(x, monthly["Total_Profit"], marker="s", color="#2ca02c", linewidth=2, linestyle="--", label="Profit ($)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly["Year_Month"], rotation=45, ha="right", fontsize=8)
    ax1.yaxis.set_major_formatter("${x:,.0f}")
    ax1.set_ylabel("USD ($)")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend()
    st.pyplot(fig)
    plt.close()

    # Quarterly Metrics
    st.write("#### Quarterly Aggregates")
    quarterly = filtered_df.groupby("Year_Quarter").agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index()
    quarterly["Margin_%"] = (quarterly["Profit"] / quarterly["Revenue"] * 100).round(2)
    st.dataframe(quarterly.style.format({
        "Revenue": "${:,.2f}",
        "Profit": "${:,.2f}",
        "Orders": "{:,}",
        "Margin_%": "{:.1f}%"
    }), use_container_width=True)

# ----- TAB 2: Category & Products ----- #
with tab2:
    st.subheader("Category & Sub-Category Diagnostics")
    cat_df = analyze_category_performance(filtered_df)
    
    c_left, c_right = st.columns([1, 1.2])
    with c_left:
        st.write("##### Category Totals")
        cat_group = filtered_df.groupby("Category").agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        ).reset_index()
        cat_group["Margin_%"] = (cat_group["Profit"] / cat_group["Sales"] * 100).round(2)
        st.dataframe(cat_group.style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}",
            "Margin_%": "{:.1f}%"
        }), use_container_width=True)

    with c_right:
        st.write("##### Sub-Category Profitability Comparison")
        fig_sub, ax_sub = plt.subplots(figsize=(6, 4))
        sub_p = cat_df.sort_values(by="Total_Profit", ascending=True)
        colors = ["#d62728" if p < 0 else "#2ca02c" for p in sub_p["Total_Profit"]]
        ax_sub.barh(sub_p["Sub_Category"], sub_p["Total_Profit"], color=colors)
        ax_sub.xaxis.set_major_formatter("${x:,.0f}")
        ax_sub.axvline(0, color="black", linestyle="--", linewidth=0.8)
        ax_sub.set_xlabel("Net Profit ($)")
        st.pyplot(fig_sub)
        plt.close()

    st.markdown("---")
    st.write("##### Top 5 Profitable vs Top 5 Loss-Making Products")
    top_rev, top_prof, worst_loss = get_top_bottom_products(filtered_df, n=5)
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.success("🏆 Most Profitable Products")
        st.dataframe(top_prof[["Product_Name", "Category", "Total_Sales", "Total_Profit", "Profit_Margin_%"]].style.format({
            "Total_Sales": "${:,.2f}",
            "Total_Profit": "${:,.2f}",
            "Profit_Margin_%": "{:.1f}%"
        }), use_container_width=True)
    with p_col2:
        st.error("⚠️ Biggest Profit Bleeders (Loss-Makers)")
        st.dataframe(worst_loss[["Product_Name", "Category", "Total_Sales", "Total_Profit", "Profit_Margin_%"]].style.format({
            "Total_Sales": "${:,.2f}",
            "Total_Profit": "${:,.2f}",
            "Profit_Margin_%": "{:.1f}%"
        }), use_container_width=True)

# ----- TAB 3: Regional Performance ----- #
with tab3:
    st.subheader("Geographic Revenue & Margin Distribution")
    reg_summary = analyze_regional_performance(filtered_df)
    
    r_col1, r_col2 = st.columns([1, 1.2])
    with r_col1:
        st.dataframe(reg_summary.style.format({
            "Total_Sales": "${:,.2f}",
            "Total_Profit": "${:,.2f}",
            "Profit_Margin_%": "{:.1f}%",
            "Sales_Share_%": "{:.1f}%",
            "Order_Count": "{:,}",
            "Units_Sold": "{:,}"
        }), use_container_width=True)
        
    with r_col2:
        fig_reg, ax_reg = plt.subplots(figsize=(6, 3.5))
        sns.barplot(data=reg_summary, x="Region", y="Total_Sales", hue="Region", legend=False, palette="Blues_r", ax=ax_reg)
        ax_reg.yaxis.set_major_formatter("${x:,.0f}")
        ax_reg.set_ylabel("Total Sales ($)")
        st.pyplot(fig_reg)
        plt.close()

# ----- TAB 4: Pricing & Discounts ----- #
with tab4:
    st.subheader("Discount Sensitivity & Profit Margin Erosion")
    st.info("💡 Strategic Insight: Orders with discounts exceeding 20% experience severe margin degradation, frequently turning transactions unprofitable.")
    
    disc_df = analyze_discount_impact(filtered_df)
    st.dataframe(disc_df.style.format({
        "Total_Sales": "${:,.2f}",
        "Total_Profit": "${:,.2f}",
        "Avg_Discount": "{:.1%}",
        "Profit_Margin_%": "{:.1f}%",
        "Loss_Rate_%": "{:.1f}%",
        "Transaction_Count": "{:,}",
        "Loss_Transactions": "{:,}"
    }), use_container_width=True)

    fig_box, ax_box = plt.subplots(figsize=(8, 3.5))
    sns.boxplot(
        data=filtered_df,
        x="Discount_Tier",
        y="Profit_Margin",
        hue="Discount_Tier",
        legend=False,
        palette="vlag",
        ax=ax_box
    )
    ax_box.axhline(0, color="red", linestyle="--", linewidth=1)
    ax_box.set_ylabel("Profit Margin %")
    ax_box.set_xlabel("Discount Tier")
    st.pyplot(fig_box)
    plt.close()

# ----- TAB 5: Data Explorer ----- #
with tab5:
    st.subheader("Transaction Explorer & Export")
    st.write(f"Displaying **{len(filtered_df):,}** transactions based on active filters.")
    
    # Download Button
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="sales_data_filtered.csv",
        mime="text/csv"
    )
    
    st.dataframe(filtered_df, use_container_width=True, height=400)

# Footer
st.caption("Sales Data Analytics Portfolio Project | Built with Python, Pandas, Matplotlib, Seaborn & Streamlit")
