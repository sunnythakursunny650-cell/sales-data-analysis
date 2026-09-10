"""
Visualization Engine
====================
Generates publication-quality, styled charts using Matplotlib and Seaborn,
saving high-resolution figures for README documentation and portfolio display.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Set professional theme defaults
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10

def setup_figure_dir(output_dir="reports/figures"):
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def plot_monthly_sales_trend(df, output_dir="reports/figures"):
    """Figure 1: Monthly Sales and Profit Trend Analysis."""
    setup_figure_dir(output_dir)
    monthly = df.groupby("Year_Month").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(12, 5))

    x = range(len(monthly))
    ax1.plot(x, monthly["Sales"], marker="o", color="#1f77b4", linewidth=2.2, label="Monthly Sales ($)")
    ax1.plot(x, monthly["Profit"], marker="s", color="#2ca02c", linewidth=2.0, linestyle="--", label="Monthly Profit ($)")
    
    ax1.set_title("Monthly Sales & Profit Performance Trend", fontsize=14, fontweight="bold", pad=12)
    ax1.set_xlabel("Year-Month", fontweight="bold")
    ax1.set_ylabel("Amount ($ USD)", fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(monthly["Year_Month"], rotation=45, ha="right", fontsize=8)
    ax1.yaxis.set_major_formatter("${x:,.0f}")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left", frameon=True)

    plt.tight_layout()
    output_path = os.path.join(output_dir, "01_monthly_sales_trend.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path

def plot_category_sales_profit(df, output_dir="reports/figures"):
    """Figure 2: Sales & Profit by Category and Sub-Category."""
    setup_figure_dir(output_dir)
    cat_summary = df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()

    sub_summary = df.groupby("Sub_Category")[["Sales", "Profit"]].sum().sort_values(by="Sales", ascending=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1, 1.8]})

    # Category comparison
    x = np.arange(len(cat_summary))
    width = 0.35
    axes[0].bar(x - width/2, cat_summary["Sales"], width, label="Sales", color="#3b528b")
    axes[0].bar(x + width/2, cat_summary["Profit"], width, label="Profit", color="#5dc863")
    axes[0].set_title("Performance by Category", fontweight="bold", fontsize=12)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(cat_summary["Category"], fontweight="bold")
    axes[0].yaxis.set_major_formatter("${x:,.0f}")
    axes[0].legend()
    axes[0].grid(axis="y", linestyle=":", alpha=0.7)

    # Sub-category horizontal bar chart
    sub_summary[["Sales", "Profit"]].plot(
        kind="barh",
        ax=axes[1],
        color=["#440154", "#21918c"],
        width=0.75
    )
    axes[1].set_title("Revenue & Profitability by Sub-Category", fontweight="bold", fontsize=12)
    axes[1].set_xlabel("Amount ($ USD)", fontweight="bold")
    axes[1].xaxis.set_major_formatter("${x:,.0f}")
    axes[1].grid(axis="x", linestyle=":", alpha=0.7)
    axes[1].legend(["Sales", "Profit"])

    plt.tight_layout()
    output_path = os.path.join(output_dir, "02_category_sales_profit.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path

def plot_regional_performance(df, output_dir="reports/figures"):
    """Figure 3: Regional Sales, Profit & Profit Margin %."""
    setup_figure_dir(output_dir)
    reg = df.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()
    reg["Profit_Margin"] = (reg["Profit"] / reg["Sales"] * 100).round(2)
    reg = reg.sort_values(by="Sales", ascending=False)

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax2 = ax1.twinx()

    colors = ["#2b5c8f", "#4682b4", "#5c9ecc", "#87ceeb"]
    bars = ax1.bar(reg["Region"], reg["Sales"], color=colors, width=0.55, alpha=0.85, label="Total Sales")
    line = ax2.plot(reg["Region"], reg["Profit_Margin"], color="#d95f02", marker="o", linewidth=2.5, markersize=8, label="Profit Margin %")

    ax1.set_title("Regional Sales Distribution & Profit Margins", fontsize=13, fontweight="bold", pad=12)
    ax1.set_xlabel("Region", fontweight="bold")
    ax1.set_ylabel("Sales ($ USD)", fontweight="bold", color="#2b5c8f")
    ax2.set_ylabel("Profit Margin (%)", fontweight="bold", color="#d95f02")
    ax1.yaxis.set_major_formatter("${x:,.0f}")
    ax2.yaxis.set_major_formatter("{x:.1f}%")
    ax1.grid(axis="y", linestyle=":", alpha=0.6)

    # Annotate bars
    for bar in bars:
        h = bar.get_height()
        ax1.annotate(f"${h:,.0f}", xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    output_path = os.path.join(output_dir, "03_regional_performance.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path

def plot_discount_vs_profitability(df, output_dir="reports/figures"):
    """Figure 4: Discount Impact on Profit Margin %."""
    setup_figure_dir(output_dir)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Boxplot of Margin by Discount Tier
    tier_order = ["No Discount (0%)", "Low (1-10%)", "Medium (11-20%)", "High (>20%)"]
    sns.boxplot(
        data=df,
        x="Discount_Tier",
        y="Profit_Margin",
        hue="Discount_Tier",
        legend=False,
        order=tier_order,
        palette="vlag",
        ax=ax1,
        showmeans=True,
        meanprops={"marker": "o", "markerfacecolor": "red", "markeredgecolor": "red"}
    )
    ax1.axhline(0, color="red", linestyle="--", linewidth=1, alpha=0.7)
    ax1.set_title("Profit Margin % by Discount Tier", fontweight="bold")
    ax1.set_xlabel("Discount Tier", fontweight="bold")
    ax1.set_ylabel("Profit Margin (%)", fontweight="bold")

    # Scatter plot Discount vs Profit Margin
    scatter = ax2.scatter(
        df["Discount"] * 100,
        df["Profit_Margin"],
        c=np.where(df["Profit"] >= 0, "#2ca02c", "#d62728"),
        alpha=0.6,
        edgecolors="none",
        s=40
    )
    ax2.axhline(0, color="black", linestyle="--", linewidth=1)
    ax2.axvline(20, color="orange", linestyle=":", linewidth=1.5, label="20% Discount Danger Threshold")
    ax2.set_title("Discount % vs Profit Margin % (Green=Profitable, Red=Loss)", fontweight="bold")
    ax2.set_xlabel("Discount Given (%)", fontweight="bold")
    ax2.set_ylabel("Profit Margin (%)", fontweight="bold")
    ax2.legend(loc="upper right")

    plt.tight_layout()
    output_path = os.path.join(output_dir, "04_discount_vs_profitability.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path

def plot_top_and_bottom_products(df, output_dir="reports/figures", n=8):
    """Figure 5: Top Profitable vs Biggest Loss-Making Products."""
    setup_figure_dir(output_dir)
    prod = df.groupby("Product_Name")[["Sales", "Profit"]].sum().reset_index()
    
    top_profit = prod.sort_values(by="Profit", ascending=False).head(n)
    bottom_profit = prod.sort_values(by="Profit", ascending=True).head(n)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Top Profitable
    sns.barplot(
        data=top_profit,
        y="Product_Name",
        x="Profit",
        hue="Product_Name",
        legend=False,
        ax=ax1,
        palette="Greens_r"
    )
    ax1.set_title(f"Top {n} Most Profitable Products", fontweight="bold", color="darkgreen")
    ax1.set_xlabel("Total Net Profit ($)", fontweight="bold")
    ax1.set_ylabel("")
    ax1.xaxis.set_major_formatter("${x:,.0f}")
    ax1.grid(axis="x", linestyle=":", alpha=0.6)

    # Bottom Loss-Makers
    sns.barplot(
        data=bottom_profit,
        y="Product_Name",
        x="Profit",
        hue="Product_Name",
        legend=False,
        ax=ax2,
        palette="Reds_r"
    )
    ax2.set_title(f"Top {n} Loss-Making Products (Profit Bleeders)", fontweight="bold", color="darkred")
    ax2.set_xlabel("Total Net Loss ($)", fontweight="bold")
    ax2.set_ylabel("")
    ax2.xaxis.set_major_formatter("${x:,.0f}")
    ax2.grid(axis="x", linestyle=":", alpha=0.6)

    plt.tight_layout()
    output_path = os.path.join(output_dir, "05_top_and_bottom_products.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path

def plot_customer_segmentation(df, output_dir="reports/figures"):
    """Figure 6: Customer Segment Sales Share and Average Order Value."""
    setup_figure_dir(output_dir)
    seg = df.groupby("Customer_Segment").agg(
        Sales=("Sales", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index()
    seg["AOV"] = seg["Sales"] / seg["Orders"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Donut chart
    colors = ["#4e79a7", "#f28e2b", "#e15759"]
    wedges, texts, autotexts = ax1.pie(
        seg["Sales"],
        labels=seg["Customer_Segment"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
        pctdistance=0.75
    )
    for autotext in autotexts:
        autotext.set_fontweight("bold")
    ax1.set_title("Sales Share by Customer Segment", fontweight="bold", fontsize=12)

    # AOV Bar Chart
    sns.barplot(
        data=seg,
        x="Customer_Segment",
        y="AOV",
        hue="Customer_Segment",
        legend=False,
        palette=colors,
        ax=ax2
    )
    ax2.set_title("Average Order Value (AOV) by Segment", fontweight="bold", fontsize=12)
    ax2.set_xlabel("Segment", fontweight="bold")
    ax2.set_ylabel("AOV ($ USD)", fontweight="bold")
    ax2.yaxis.set_major_formatter("${x:,.0f}")
    ax2.grid(axis="y", linestyle=":", alpha=0.6)

    for p in ax2.patches:
        val = p.get_height()
        ax2.annotate(f"${val:,.2f}", (p.get_x() + p.get_width() / 2., val),
                     ha="center", va="bottom", fontsize=9, xytext=(0, 3), textcoords="offset points")

    plt.tight_layout()
    output_path = os.path.join(output_dir, "06_customer_segmentation.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path

def generate_all_visualizations(df, output_dir="reports/figures"):
    """Generates and saves the complete portfolio chart suite."""
    print("[Visualization Engine] Rendering and saving portfolio charts...")
    paths = []
    paths.append(plot_monthly_sales_trend(df, output_dir))
    paths.append(plot_category_sales_profit(df, output_dir))
    paths.append(plot_regional_performance(df, output_dir))
    paths.append(plot_discount_vs_profitability(df, output_dir))
    paths.append(plot_top_and_bottom_products(df, output_dir))
    paths.append(plot_customer_segmentation(df, output_dir))
    print(f"[Visualization Engine] All {len(paths)} charts saved to '{output_dir}/'")
    return paths

if __name__ == "__main__":
    from data_cleaning import clean_sales_data
    df = clean_sales_data()
    generate_all_visualizations(df)
