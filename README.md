# Supply Chain Analytics Dashboard

> Analyzed **180,519 real supply chain orders** to find out why **57% of deliveries are late** - and what to do about it.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-red)](https://streamlit.io)
[![SQL](https://img.shields.io/badge/SQL-SQLite-orange)]()
[![Framework](https://img.shields.io/badge/Framework-Lean%20Six%20Sigma%20DMAIC-green)]()

---

## 🔴 Live Dashboard

👉 **(https://karan-supply-chain.streamlit.app/)**

> **note on data:** Full analysis was run locally on all 180,519 real orders.
> The live dashboard uses a 50,000 order sample — all 23 regions, all shipping modes,
> all customer segments fully represented. The findings are consistent with the full dataset.
> Full SQL query outputs are available in the `/outputs/sql` folder.

---

## The Problem

I built this because late deliveries are one of the most expensive and preventable problems in supply chain management.

When I ran the analysis on 180,519 real orders, the number that came back stopped me:

**Only 42.7% of orders are delivered on time. 103,400 orders — more than half — arrived late.**

That is not a small operational issue. That is a systemic failure that costs companies millions in customer satisfaction, returns, and repeat business. This dashboard identifies exactly where the failures happen and what to fix first.

---

## What I Found

| Finding | Detail |
|---------|--------|
| On-time delivery rate | **42.7%** - industry standard is 85%+ |
| Total late orders | **103,400** out of 180,519 |
| Worst performing region | **Central Africa - 60.7% late rate** |
| Best performing region | **Canada - 51.9% late rate** |
| Highest revenue category | **Fishing - $2.4M+** |
| Average profit margin | **12.1%** across all categories |
| Total revenue analyzed | **$36.7 million** |
| Date range | January 2015 - January 2018 |

---

## 📊 Dashboard - 5 Tabs

### Tab 1 - Executive Summary
The C-suite view. Late delivery rate by region and shipping mode side by side.
The story is immediate — every region is failing, but some are worse than others.

### Tab 2 - Delivery Performance
Where exactly are we failing? Late delivery breakdown by region with a distribution
chart showing how bad the delays actually are. Most late orders are only 1-2 days
late — which means this is fixable with better carrier management, not a structural problem.

### Tab 3 - Revenue & Profit
Which product categories make the most money? Which customer segments spend the most?
Monthly sales trend showing seasonality patterns across 3 years of real data.

### Tab 4 - ABC Inventory Segmentation
Classic supply chain Six Sigma tool applied to real data. Class A products generate
80% of revenue from a small number of SKUs — these need priority stock protection.
Class C products are consuming logistics bandwidth without proportional return.

### Tab 5 - DMAIC Six Sigma Report
This tab is what makes this project different from every other supply chain dashboard
on GitHub. Full Lean Six Sigma structured analysis — Define, Measure, Analyze, Improve,
Control — applied to the data findings. This is how a Black Belt thinks about a problem.

---

## SQL Analysis - 15 Business Queries

Beyond the dashboard, I loaded the full dataset into SQLite and wrote 15 SQL queries
answering real business questions. Results are saved as CSV files in `/outputs/sql/`.

```sql
-- Sample queries included:
-- Q1:  Late delivery rate by region — ranked worst to best
-- Q2:  Top 15 revenue categories with profit margins
-- Q3:  Customer segment revenue and order value analysis
-- Q4:  Shipping mode performance — which carrier is failing most?
-- Q5:  Top 20 products by revenue with margin breakdown
-- Q6:  Monthly revenue trend — 2015 to 2018
-- Q7:  Market performance — which global market is most profitable?
-- Q8:  Department revenue and margin analysis
-- Q9:  Top 20 highest value customers
-- Q10: Delivery status distribution across all orders
-- Q11: Revenue and profit by payment type
-- Q12: Late orders by category — revenue at risk calculation
-- Q13: Order status analysis — cancelled, pending, complete
-- Q14: Region revenue ranking using SQL window functions (RANK OVER)
-- Q15: Executive KPI summary — single query, all key metrics
```

---

## Tech Stack

```
Python 3.11      — Core analysis and dashboard
Pandas           — Data processing (180,519 orders)
Plotly           — Interactive visualizations
Streamlit        — Live dashboard deployment
SQL + SQLite     — 15 business queries on full dataset
Lean Six Sigma   — DMAIC analytical framework (Black Belt)
```

---

## 📁Project Structure

```
supply-chain-analytics/
│
├── data/
│   ├── DataCoSupplyChainDataset.csv    ← full dataset (not uploaded — 95MB)
│   └── supply_chain_sample.csv         ← 50k sample for cloud dashboard
│
├── outputs/
│   ├── 01_late_delivery_by_region.html
│   ├── 02_late_delivery_by_shipping_mode.html
│   ├── 03_revenue_by_category.html
│   ├── 04_customer_segment_revenue.html
│   ├── 05_monthly_sales_trend.html
│   ├── 06_abc_inventory_segmentation.html
│   └── sql/
│       ├── Q1_Late_Rate_By_Region.csv
│       ├── Q2_Revenue_By_Category.csv
│       └── ... (15 SQL query outputs)
│
├── dashboard.py       ← Streamlit dashboard
├── analyze.py         ← Full Python analysis (180k orders)
├── sql_analysis.py    ← 15 SQL queries via SQLite
├── requirements.txt
└── README.md
```

---

## How To Run Locally

```bash
git clone https://github.com/Karant15/Supply-Chain-Analytics.git
cd Supply-Chain-Analytics
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Download full dataset from Mendeley Data (link below) → place in /data folder

# Run full Python analysis
python analyze.py

# Run SQL analysis
python sql_analysis.py

# Launch dashboard
streamlit run dashboard.py
```

---

## DMAIC Summary

| Phase | Action | Finding |
|-------|--------|---------|
| **Define** | Set problem scope | 57.3% late delivery rate - goal: 70%+ on time |
| **Measure** | Baseline KPIs | 103,400 late orders - $36.7M revenue analyzed |
| **Analyze** | Root cause identification | Central Africa worst (60.7%) - First Class shipping has the highest late rate |
| **Improve** | Recommendations | Carrier SLA enforcement + regional logistics partner review + Class C SKU reduction |
| **Control** | Monitoring | This live dashboard - filter by region, segment, year in real time |

---

## 💡 Why I Built This

Before my MS in Data Analytics I spent 5 years managing client accounts with 30+ NHS hospitals in the UK. Supply chain and staffing analytics were part of every conversation — which hospitals were running low on specialists, which logistics routes were failing, which procurement decisions were draining budgets.

This project brings that domain knowledge together with real data science. It is not just a dashboard — it is a decision-making tool built the way a Six Sigma Black Belt would build it.

---

## 👤 About

**Karan Trivedi** | MS Data Analytics, Webster University (Dec 2024)
- Lean Six Sigma Black Belt — Benchmark Six Sigma (2021)
- 7+ years healthcare, recruitment, and business analytics
- Former Senior Accounts Manager — 30+ NHS hospital accounts

📧 krntrivedi@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/karan-r-trivedi-b9a96a56)
🏥 [Healthcare Project](https://karan-healthcare-analytics.streamlit.app)
🐙 [GitHub](https://github.com/Karant15)

---

## 📄 Data Source

**DataCo Smart Supply Chain for Big Data Analysis**
- Source: [Mendeley Data](https://data.mendeley.com/datasets/8gx2fvg2k6/5)
- Records: 180,519 orders × 53 columns
- Coverage: 23 global regions | Multiple markets | 2015–2018
- License: CC BY 4.0 - open research data
