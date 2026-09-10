"""
Business Analysis & Metrics Engine
===================================
Computes executive KPIs, time-series growth rates, category profitability,
regional breakdowns, discount sensitivity, and customer segment metrics.
"""

import pandas as pd
import numpy as np

def calculate_executive_kpis(df):
    """Computes high-level business performance KPIs."""
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0.0
    total_orders = df["Order_ID"].nunique()
    total_units = df["Quantity"].sum()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0
    avg_shipping_days = df["Shipping_Days"].mean()
    profitable_orders = (df["Profit"] > 0).sum()
    profitable_order_rate = (profitable_orders / len(df) * 100) if len(df) > 0 else 0.0

    return {
        "Total Sales": round(total_sales, 2),
        "Total Profit": round(total_profit, 2),
        "Profit Margin %": round(profit_margin, 2),
        "Total Orders": total_orders,
        "Total Units Sold": total_units,
        "Average Order Value (AOV)": round(avg_order_value, 2),
        "Average Shipping Lead Time (Days)": round(avg_shipping_days, 1),
        "Profitable Transactions Rate %": round(profitable_order_rate, 1)
    }

def analyze_monthly_trends(df):
    """Computes monthly aggregate sales, profit, and MoM growth rates."""
    monthly = df.groupby("Year_Month").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Order_Count=("Order_ID", "nunique"),
        Units_Sold=("Quantity", "sum")
    ).reset_index()

    monthly["Sales_MoM_Growth_%"] = monthly["Total_Sales"].pct_change() * 100
    monthly["Profit_MoM_Growth_%"] = monthly["Total_Profit"].pct_change() * 100
    monthly["Profit_Margin_%"] = (monthly["Total_Profit"] / monthly["Total_Sales"] * 100).round(2)

    return monthly

def analyze_category_performance(df):
    """Aggregates sales and profitability by product category and sub-category."""
    cat_summary = df.groupby(["Category", "Sub_Category"]).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum"),
        Order_Count=("Order_ID", "count"),
        Avg_Discount=("Discount", "mean")
    ).reset_index()

    cat_summary["Profit_Margin_%"] = (cat_summary["Total_Profit"] / cat_summary["Total_Sales"] * 100).round(2)
    cat_summary["Is_Loss_Maker"] = cat_summary["Total_Profit"] < 0
    cat_summary = cat_summary.sort_values(by="Total_Sales", ascending=False).reset_index(drop=True)

    return cat_summary

def analyze_regional_performance(df):
    """Analyzes geographic revenue, profits, and margin across regions."""
    reg_summary = df.groupby("Region").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Order_Count=("Order_ID", "nunique"),
        Units_Sold=("Quantity", "sum")
    ).reset_index()

    reg_summary["Profit_Margin_%"] = (reg_summary["Total_Profit"] / reg_summary["Total_Sales"] * 100).round(2)
    reg_summary["Sales_Share_%"] = (reg_summary["Total_Sales"] / reg_summary["Total_Sales"].sum() * 100).round(2)
    reg_summary = reg_summary.sort_values(by="Total_Sales", ascending=False).reset_index(drop=True)

    return reg_summary

def analyze_discount_impact(df):
    """Evaluates how discount intensity correlates with sales and profit margins."""
    tier_order = ["No Discount (0%)", "Low (1-10%)", "Medium (11-20%)", "High (>20%)"]
    
    disc_summary = df.groupby("Discount_Tier").agg(
        Transaction_Count=("Order_ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Avg_Discount=("Discount", "mean"),
        Loss_Transactions=("Profit", lambda x: (x < 0).sum())
    ).reindex(tier_order).reset_index()

    disc_summary["Profit_Margin_%"] = (disc_summary["Total_Profit"] / disc_summary["Total_Sales"] * 100).round(2)
    disc_summary["Loss_Rate_%"] = (disc_summary["Loss_Transactions"] / disc_summary["Transaction_Count"] * 100).round(1)

    return disc_summary

def analyze_customer_segments(df):
    """Breaks down performance by Customer Segment (Consumer, Corporate, Home Office)."""
    seg_summary = df.groupby("Customer_Segment").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order_ID", "nunique"),
        Units_Sold=("Quantity", "sum")
    ).reset_index()

    seg_summary["Sales_Share_%"] = (seg_summary["Total_Sales"] / seg_summary["Total_Sales"].sum() * 100).round(2)
    seg_summary["Profit_Margin_%"] = (seg_summary["Total_Profit"] / seg_summary["Total_Sales"] * 100).round(2)
    seg_summary["AOV"] = (seg_summary["Total_Sales"] / seg_summary["Total_Orders"]).round(2)

    return seg_summary

def get_top_bottom_products(df, n=10):
    """Identifies top revenue, top profit, and biggest loss-making products."""
    prod_summary = df.groupby(["Product_ID", "Product_Name", "Category", "Sub_Category"]).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum"),
        Avg_Discount=("Discount", "mean")
    ).reset_index()

    prod_summary["Profit_Margin_%"] = (prod_summary["Total_Profit"] / prod_summary["Total_Sales"] * 100).round(2)

    top_revenue = prod_summary.sort_values(by="Total_Sales", ascending=False).head(n)
    top_profitable = prod_summary.sort_values(by="Total_Profit", ascending=False).head(n)
    worst_loss_makers = prod_summary[prod_summary["Total_Profit"] < 0].sort_values(by="Total_Profit", ascending=True).head(n)

    return top_revenue, top_profitable, worst_loss_makers
