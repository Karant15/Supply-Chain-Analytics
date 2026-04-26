import pandas as pd
import sqlite3
import os
import warnings
warnings.filterwarnings('ignore')

print("Loading data into SQLite database...")
df = pd.read_csv(
    r'C:\Users\13142\Desktop\supply-chain-analytics\data\DataCoSupplyChainDataset.csv',
    encoding='latin-1'
)

conn = sqlite3.connect('supply_chain.db')
df.to_sql('orders', conn, if_exists='replace', index=False)
print(f"Database created: {len(df):,} orders loaded")

queries = {
    "Q1_Late_Rate_By_Region": """
        SELECT [Order Region],
            COUNT(*) as Total_Orders,
            SUM(Late_delivery_risk) as Late_Orders,
            ROUND(SUM(Late_delivery_risk) * 100.0 / COUNT(*), 1) as Late_Rate_Pct
        FROM orders
        GROUP BY [Order Region]
        ORDER BY Late_Rate_Pct DESC
    """,
    "Q2_Revenue_By_Category": """
        SELECT [Category Name],
            COUNT(*) as Total_Orders,
            ROUND(SUM(Sales), 2) as Total_Revenue,
            ROUND(AVG(Sales), 2) as Avg_Order_Value,
            ROUND(SUM([Order Profit Per Order]), 2) as Total_Profit
        FROM orders
        GROUP BY [Category Name]
        ORDER BY Total_Revenue DESC
        LIMIT 15
    """,
    "Q3_Customer_Segment_Analysis": """
        SELECT [Customer Segment],
            COUNT(DISTINCT [Customer Id]) as Unique_Customers,
            COUNT(*) as Total_Orders,
            ROUND(SUM(Sales), 2) as Total_Revenue,
            ROUND(AVG(Sales), 2) as Avg_Order_Value,
            ROUND(SUM([Order Profit Per Order]), 2) as Total_Profit
        FROM orders
        GROUP BY [Customer Segment]
        ORDER BY Total_Revenue DESC
    """,
    "Q4_Shipping_Mode_Performance": """
        SELECT [Shipping Mode],
            COUNT(*) as Total_Orders,
            SUM(Late_delivery_risk) as Late_Orders,
            ROUND(SUM(Late_delivery_risk) * 100.0 / COUNT(*), 1) as Late_Rate_Pct,
            ROUND(AVG([Days for shipping (real)]), 1) as Avg_Actual_Days,
            ROUND(AVG([Days for shipment (scheduled)]), 1) as Avg_Scheduled_Days
        FROM orders
        GROUP BY [Shipping Mode]
        ORDER BY Late_Rate_Pct DESC
    """,
    "Q5_Top_Revenue_Products": """
        SELECT [Product Name],
            COUNT(*) as Times_Ordered,
            ROUND(SUM(Sales), 2) as Total_Revenue,
            ROUND(AVG(Sales), 2) as Avg_Price,
            ROUND(SUM([Order Profit Per Order]), 2) as Total_Profit,
            ROUND(AVG([Order Item Profit Ratio]) * 100, 1) as Avg_Margin_Pct
        FROM orders
        GROUP BY [Product Name]
        ORDER BY Total_Revenue DESC
        LIMIT 20
    """,
    "Q6_Monthly_Revenue_Trend": """
        SELECT SUBSTR([order date (DateOrders)], 1, 7) as Year_Month,
            COUNT(*) as Total_Orders,
            ROUND(SUM(Sales), 2) as Total_Revenue,
            ROUND(AVG(Sales), 2) as Avg_Order_Value,
            SUM(Late_delivery_risk) as Late_Orders
        FROM orders
        WHERE [order date (DateOrders)] IS NOT NULL
        GROUP BY SUBSTR([order date (DateOrders)], 1, 7)
        ORDER BY Year_Month
    """,
    "Q7_Market_Performance": """
        SELECT Market,
            COUNT(*) as Total_Orders,
            ROUND(SUM(Sales), 2) as Total_Revenue,
            ROUND(SUM([Order Profit Per Order]), 2) as Total_Profit,
            ROUND(SUM(Late_delivery_risk) * 100.0 / COUNT(*), 1) as Late_Rate_Pct
        FROM orders
        GROUP BY Market
        ORDER BY Total_Revenue DESC
    """,
    "Q8_Department_Analysis": """
        SELECT [Department Name],
            COUNT(*) as Total_Orders,
            ROUND(SUM(Sales), 2) as Total_Revenue,
            ROUND(AVG([Order Item Profit Ratio]) * 100, 1) as Avg_Margin_Pct,
            SUM(Late_delivery_risk) as Late_Orders
        FROM orders
        GROUP BY [Department Name]
        ORDER BY Total_Revenue DESC
    """,
    "Q9_High_Value_Customers": """
        SELECT [Customer Id],
            [Customer Segment],
            [Customer City],
            [Customer State],
            COUNT(*) as Total_Orders,
            ROUND(SUM(Sales), 2) as Total_Spent,
            ROUND(AVG(Sales), 2) as Avg_Order_Value
        FROM orders
        GROUP BY [Customer Id]
        ORDER BY Total_Spent DESC
        LIMIT 20
    """,
    "Q10_Delivery_Status_Summary": """
        SELECT [Delivery Status],
            COUNT(*) as Total_Orders,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 1) as Pct_Of_Total,
            ROUND(SUM(Sales), 2) as Total_Revenue
        FROM orders
        GROUP BY [Delivery Status]
        ORDER BY Total_Orders DESC
    """,
    "Q11_Profit_By_Payment_Type": """
        SELECT Type as Payment_Type,
            COUNT(*) as Total_Orders,
            ROUND(SUM(Sales), 2) as Total_Revenue,
            ROUND(SUM([Order Profit Per Order]), 2) as Total_Profit,
            ROUND(AVG([Order Item Profit Ratio]) * 100, 1) as Avg_Margin_Pct
        FROM orders
        GROUP BY Type
        ORDER BY Total_Revenue DESC
    """,
    "Q12_Late_Orders_By_Category": """
        SELECT [Category Name],
            COUNT(*) as Total_Orders,
            SUM(Late_delivery_risk) as Late_Orders,
            ROUND(SUM(Late_delivery_risk) * 100.0 / COUNT(*), 1) as Late_Rate_Pct,
            ROUND(SUM(Sales), 2) as Revenue_At_Risk
        FROM orders
        GROUP BY [Category Name]
        ORDER BY Revenue_At_Risk DESC
        LIMIT 15
    """,
    "Q13_Order_Status_Analysis": """
        SELECT [Order Status],
            COUNT(*) as Total_Orders,
            ROUND(SUM(Sales), 2) as Total_Revenue,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 1) as Pct_Of_Total
        FROM orders
        GROUP BY [Order Status]
        ORDER BY Total_Orders DESC
    """,
    "Q14_Region_Revenue_Ranking": """
        SELECT [Order Region], Market,
            COUNT(*) as Total_Orders,
            ROUND(SUM(Sales), 2) as Total_Revenue,
            ROUND(SUM([Order Profit Per Order]), 2) as Total_Profit
        FROM orders
        GROUP BY [Order Region], Market
        ORDER BY Total_Revenue DESC
    """,
    "Q15_Executive_KPI_Summary": """
        SELECT
            COUNT(*) as Total_Orders,
            COUNT(DISTINCT [Customer Id]) as Unique_Customers,
            COUNT(DISTINCT [Product Name]) as Unique_Products,
            COUNT(DISTINCT [Order Region]) as Regions_Served,
            ROUND(SUM(Sales), 2) as Total_Revenue,
            ROUND(SUM([Order Profit Per Order]), 2) as Total_Profit,
            ROUND(AVG([Order Item Profit Ratio]) * 100, 1) as Avg_Margin_Pct,
            SUM(Late_delivery_risk) as Total_Late_Orders,
            ROUND(SUM(Late_delivery_risk) * 100.0 / COUNT(*), 1) as Overall_Late_Rate_Pct
        FROM orders
    """
}

print("\nRunning 15 SQL queries...")
os.makedirs('outputs/sql', exist_ok=True)

for name, query in queries.items():
    result = pd.read_sql_query(query, conn)
    result.to_csv(f'outputs/sql/{name}.csv', index=False)
    print(f"  ✓ {name} — {len(result)} rows")

conn.close()

print("\nKEY FINDINGS FROM SQL:")
conn2 = sqlite3.connect('supply_chain.db')
kpi = pd.read_sql_query(queries['Q15_Executive_KPI_Summary'], conn2)
print(kpi.to_string(index=False))
conn2.close()
print("\nAll 15 SQL results saved in outputs/sql/")