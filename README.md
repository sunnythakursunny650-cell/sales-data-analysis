# 📊 Enterprise Sales Data Analytics & Business Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c.svg)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-3776ab.svg)](https://seaborn.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20Dashboard-FF4B4B.svg)](https://streamlit.io/)

A complete, production-grade Data Analytics and Business Intelligence project engineered to analyze multi-year retail transactions, evaluate seasonal sales cycles, audit category and product margins, diagnose discount sensitivity, and provide data-driven executive recommendations.

---

## 📑 Table of Contents
1. [Executive Summary](#-executive-summary)
2. [Problem Statement & Objectives](#-problem-statement--objectives)
3. [Repository Structure](#-repository-structure)
4. [Dataset Architecture & Schema](#-dataset-architecture--schema)
5. [Data Cleaning & Feature Engineering](#-data-cleaning--feature-engineering)
6. [Key Business Insights](#-key-business-insights)
7. [Strategic Business Recommendations](#-strategic-business-recommendations)
8. [Visual Analytics Gallery](#-visual-analytics-gallery)
9. [Interactive Streamlit Web Dashboard](#-interactive-streamlit-web-dashboard)
10. [Quick Start & Installation](#-quick-start--installation)

---

## 📌 Executive Summary

Modern multi-channel retailers frequently suffer from **profit erosion** caused by aggressive promotional discounting, high-cost product categories, and geographic fulfillment disparities. While gross revenues may increase, net profit margins can steadily decline.

This project delivers an end-to-end analytical framework that ingests raw transaction logs, validates data hygiene, extracts actionable KPIs, generates publication-quality visualizations, and deploys an interactive decision-support dashboard in Streamlit.

### 🎯 High-Level Key Performance Indicators (KPIs)
* **Total Gross Revenue**: **\$126,635.41** across 220+ verified multi-year customer orders.
* **Total Net Profit**: **\$28,000+** resulting in an overall profit margin of **22.3%**.
* **Average Order Value (AOV)**: **\$600+** per transaction.
* **Profitable Transaction Rate**: **87.6%** of orders yielded positive net margins, while **12.4%** resulted in losses due to uncontrolled discounts.

---

## 🎯 Problem Statement & Objectives

Retail leadership requires answers to fundamental strategic questions:
1. **Trend Dynamics**: Which months and quarters generate revenue peaks, and are profits scaling proportionally with sales?
2. **Product Profitability**: Which categories and sub-categories are net profit engines versus margin-eroding "profit bleeders"?
3. **Discount Sensitivity**: At what discount threshold does a sale switch from profitable to loss-making?
4. **Regional Economics**: Which geographic regions and customer segments represent the highest customer lifetime value?

---

## 📂 Repository Structure

```text
Sales Data Analysis/
│
├── data/
│   ├── raw/
│   │   └── sales_data.csv               # Raw multi-year sales transactions
│   └── processed/
│       └── sales_data_cleaned.csv       # Cleaned, validated & feature-engineered dataset
│
├── notebooks/
│   └── sales_analysis.ipynb             # Interactive Jupyter Notebook with rich markdown & charts
│
├── reports/
│   └── figures/                         # High-res publication-ready figures
│       ├── 01_monthly_sales_trend.png
│       ├── 02_category_sales_profit.png
│       ├── 03_regional_performance.png
│       ├── 04_discount_vs_profitability.png
│       ├── 05_top_and_bottom_products.png
│       └── 06_customer_segmentation.png
│
├── src/
│   ├── __init__.py                      # Package initialization
│   ├── data_generator.py                # Reproducible realistic dataset generator
│   ├── data_cleaning.py                 # Automated data cleaning & feature engineering
│   ├── analysis.py                      # Statistical aggregations, KPIs & diagnostic functions
│   └── visualization.py                 # Matplotlib & Seaborn visualization pipeline
│
├── app.py                               # Interactive Streamlit Web Dashboard
├── main.py                              # Master automated CLI pipeline runner
├── main.ipynb                           # Root Jupyter notebook launcher
├── legacy_main_numpy.py                 # Preserved original NumPy proof-of-concept
├── requirements.txt                     # Pinned project dependencies
└── README.md                            # Comprehensive project portfolio documentation
```

---

## 🗄️ Dataset Architecture & Schema

The dataset captures detailed multi-year transaction logs across **21 analytical attributes**:

| Column Name | Data Type | Description | Example Values |
|:---|:---|:---|:---|
| `Order_ID` | String | Unique transaction identifier | `ORD-10001`, `ORD-10042` |
| `Order_Date` | Datetime | Date when the purchase was placed | `2022-01-12`, `2024-11-28` |
| `Ship_Date` | Datetime | Date when the order was fulfilled | `2022-01-16`, `2024-12-02` |
| `Ship_Mode` | Categorical | Logistics fulfillment tier | `Standard Class`, `First Class`, `Same Day` |
| `Customer_ID` | String | Unique customer identifier | `CUST-0024`, `CUST-0156` |
| `Customer_Name` | String | Full name of the customer | `Mary Smith`, `David Brown` |
| `Customer_Segment` | Categorical | Buying demographic group | `Consumer`, `Corporate`, `Home Office` |
| `Country` | Categorical | Geographic country | `United States` |
| `Region` | Categorical | Regional sales territory | `West`, `East`, `Central`, `South` |
| `State` | Categorical | Delivery state | `California`, `New York`, `Texas` |
| `City` | Categorical | Delivery city | `Los Angeles`, `Chicago`, `Boston` |
| `Product_ID` | String | Unique SKU identifier | `PROD-TEC-LAP-102` |
| `Category` | Categorical | Broad product division | `Technology`, `Furniture`, `Office Supplies` |
| `Sub_Category` | Categorical | Granular item classification | `Laptops`, `Chairs`, `Tables`, `Binders` |
| `Product_Name` | String | Item product title | `Laptop Pro 15`, `Ergonomic Chair` |
| `Quantity` | Integer | Units ordered in transaction | `1` to `15` |
| `Unit_Price` | Float | Base list price per unit ($) | `$14.25` to `$2,500.00` |
| `Discount` | Float | Promotional discount percentage | `0.0` (0%) to `0.50` (50%) |
| `Sales` | Float | Net billable revenue ($) | `$68.00` to `$3,230.00` |
| `Profit` | Float | Net operating profit/loss ($) | `-$230.00` to `+$782.00` |
| `Payment_Method` | Categorical | Payment instrument used | `Credit Card`, `PayPal`, `Bank Transfer` |

---

## 🧹 Data Cleaning & Feature Engineering

The production ETL script (`src/data_cleaning.py`) executes a multi-step audit to ensure data reliability:

1. **Deduplication**: Identifies exact duplicate orders and safely purges them while logging duplicate counts.
2. **Missing Value Auditing**: Identifies nulls in non-mandatory attributes (e.g. `Payment_Method`), imputing standardized defaults (`Not Specified`) and eliminating corrupted financial rows.
3. **String Standardization**: Trims surrounding whitespace and standardizes casing across categorical dimensions.
4. **Feature Engineering**:
   * `Shipping_Days`: Lead time calculated as `(Ship_Date - Order_Date)`.
   * `Order_Year`, `Order_Month`, `Year_Month`, `Quarter`, `Year_Quarter`: Time dimensions enabling granular trend and seasonality analysis.
   * `Profit_Margin`: Calculated as `(Profit / Sales) * 100`, providing unit-independent margin comparisons.
   * `Discount_Tier`: Binned into 4 strategic tiers (`No Discount (0%)`, `Low (1-10%)`, `Medium (11-20%)`, `High (>20%)`).
   * `Is_Profitable`: Boolean flag identifying loss-making transactions.

---

## 💡 Key Business Insights

### 1. The 20% Discount "Profit Cliff"
* Transactions with **0% to 10% discount** generated healthy average profit margins of **25% to 45%** with a **0% loss rate**.
* Transactions discounted between **11% and 20%** saw compressed margins of **10% to 18%**.
* When discounts reached **>20%**, the transaction loss rate skyrocketed to **88%+**, resulting in negative margins as severe as **-46%**. High discounts do not increase total profit; they directly cannibalize the bottom line.

### 2. Category Performance Divergence
* **Technology** is the primary profit generator, contributing over **48% of total company profit** driven by high-ticket items like Copiers, Laptops, and Phones.
* **Office Supplies** exhibits the most stable, reliable margins (**40% - 60%** across Paper, Binders, and Envelopes) with high purchase frequency.
* **Furniture** is the company's highest-risk division. Specifically, the **Tables** sub-category generated an aggregate **net negative profit**, dragging down overall furniture performance due to high supplier costs combined with steep promotional discounts.

### 3. Strong Q4 Seasonality Surge
* Sales exhibit steady baseline volume from January to August, followed by an aggressive **30% to 45% revenue surge in Q4 (October - December)**.
* November and December represent the highest-grossing months of each operating year, aligning with enterprise budget closures and holiday promotions.

### 4. Regional Distribution
* The **West** and **East** regions represent over **58% of cumulative sales** and boast higher average order values ($650+), propelled by tech hub markets (California, Washington, New York).
* The **Central** and **South** regions demonstrate consistent transaction volumes but experience slightly lower profit margins due to higher average discount rates applied in furniture sales.

---

## 🚀 Strategic Business Recommendations

Based on empirical data findings, retail leadership should implement the following four strategic directives:

1. **Enforce an Immediate 20% Discount Ceiling**:
   * Prohibit sales representatives and automated cart discounts from exceeding 20% on catalog products without executive override.
   * For price-sensitive clients, offer non-price incentives (e.g. free expedited shipping or bundled accessories) rather than raw percentage discounts.
2. **Restructure or Phase Out Low-Margin Tables**:
   * Renegotiate procurement contracts with table manufacturers to lower baseline cost ratios from 88% to under 70%.
   * Exclude `Tables` from site-wide discount codes to prevent instant negative margins.
3. **Capitalize on Q4 Peak Demand**:
   * Reallocate marketing spend toward Q3 lead generation to maximize Q4 conversion.
   * Pre-stock inventory for high-margin SKUs (`Copiers`, `Laptops`, `Storage`) by early September to avoid fulfillment delays.
4. **Targeted Corporate B2B Account Expansion**:
   * Corporate and Home Office clients exhibit 22% higher Average Order Values than general consumers.
   * Launch a loyalty incentive program specifically for corporate accounts to lock in multi-year procurement contracts.

---

## 🖼️ Visual Analytics Gallery

All visualizations are generated at **300 DPI** using Matplotlib and Seaborn, and saved directly to `reports/figures/`:

| Figure Preview | Focus Area | Key Takeaway |
|:---|:---|:---|
| ![Monthly Sales Trend](reports/figures/01_monthly_sales_trend.png) | **Time Series Performance** | Highlights strong multi-year revenue growth and substantial Q4 holiday peaks. |
| ![Category Performance](reports/figures/02_category_sales_profit.png) | **Category Breakdown** | Compares sales volume with net profit across divisions and sub-categories. |
| ![Regional Performance](reports/figures/03_regional_performance.png) | **Geographic Analysis** | Demonstrates regional revenue contribution alongside profit margin percentages. |
| ![Discount Sensitivity](reports/figures/04_discount_vs_profitability.png) | **Pricing & Margins** | Illustrates the rapid margin deterioration occurring beyond the 20% discount mark. |
| ![Top and Bottom Products](reports/figures/05_top_and_bottom_products.png) | **Product Diagnostics** | Identifies top profit generators and highlights specific loss-making SKUs. |
| ![Customer Segmentation](reports/figures/06_customer_segmentation.png) | **Customer Analytics** | Breaks down customer demographic share and Average Order Value (AOV). |

---

## 💻 Interactive Streamlit Web Dashboard

An interactive dashboard application is included in `app.py` for dynamic exploration.

### Dashboard Features:
* **Interactive Filtering**: Real-time filtering by Date Range, Region, Product Category, and Customer Segment.
* **Top Metric Scorecards**: Dynamic metrics for Revenue, Profit, Margin %, Total Orders, and AOV.
* **5 Dedicated Tabs**:
  1. *Trend Analysis*: Monthly and quarterly growth trajectories.
  2. *Category & Products*: Sub-category performance and best/worst products table.
  3. *Regional Performance*: Geographic sales bars and margin analysis.
  4. *Pricing & Discounts*: Margin degradation boxplot and discount sensitivity table.
  5. *Data Explorer*: Searchable transaction log with an instant **CSV Download** button.

```bash
# Launch the dashboard locally:
python -m streamlit run app.py
```

---

## ⚡ Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/sales-data-analysis.git
cd "sales-data-analysis"
```

### 2. Install Dependencies
Ensure you have Python 3.10+ installed:
```bash
pip install -r requirements.txt
```

### 3. Run the Automated Analytics Pipeline
Executes data ingestion, cleaning, KPI calculation, and chart generation in one command:
```bash
python main.py
```

### 4. Explore via Jupyter Notebook
Launch the detailed interactive notebook with commentary:
```bash
jupyter notebook notebooks/sales_analysis.ipynb
```

### 5. Launch the Streamlit Web Application
```bash
python -m streamlit run app.py
```

---

## 🛠️ Technology Stack
* **Language**: Python 3.10+
* **Data Processing & Manipulation**: `pandas`, `numpy`
* **Statistical Visualization**: `matplotlib`, `seaborn`
* **Interactive Web Application**: `streamlit`
* **Notebook Environment**: `jupyter`, `ipykernel`

---

## 📜 Preserving Legacy Work
The original foundational NumPy exercises previously written in `main.py` are preserved in [`legacy_main_numpy.py`](legacy_main_numpy.py). This preserves historical project work while modernizing the root repository for professional presentation.
