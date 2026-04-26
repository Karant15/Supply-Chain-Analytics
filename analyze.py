import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
import os
warnings.filterwarnings('ignore')

# ── LOAD DATA ───────────────────────────────────────────────────
print("Loading 180,519 real supply chain orders...")
df = pd.read_csv(
    r'C:\Users\13142\Desktop\supply-chain-analytics\data\DataCoSupplyChainDataset.csv',
    encoding='latin-1'
)
print(f"Loaded: {df.shape[0]:,} orders x {df.shape[1]} columns")

# ── CLEAN DATA ──────────────────────────────────────────────────
print("\nCleaning data...")

# Drop columns we don't need
drop_cols = ['Customer Email', 'Customer Password', 'Customer Street',
             'Product Description', 'Product Image']
df = df.drop(columns=drop_cols)

# Fix date columns
df['order date (DateOrders)'] = pd.to_datetime(
    df['order date (DateOrders)'], errors='coerce'
)
df['shipping date (DateOrders)'] = pd.to_datetime(
    df['shipping date (DateOrders)'], errors='coerce'
)

# Create useful columns
df['Order Year']  = df['order date (DateOrders)'].dt.year
df['Order Month'] = df['order date (DateOrders)'].dt.month
df['Order Month Name'] = df['order date (DateOrders)'].dt.strftime('%b')
df['Is Late'] = (df['Days for shipping (real)'] >
                 df['Days for shipment (scheduled)']).astype(int)
df['Shipping Delay Days'] = (df['Days for shipping (real)'] -
                              df['Days for shipment (scheduled)'])

print(f"After cleaning: {df.shape[0]:,} rows")
print(f"Date range: {df['order date (DateOrders)'].min().date()} "
      f"to {df['order date (DateOrders)'].max().date()}")

# ── BASELINE KPIs ───────────────────────────────────────────────
print("\nCalculating baseline KPIs...")
total_orders    = len(df)
late_orders     = df['Is Late'].sum()
on_time_rate    = ((total_orders - late_orders) / total_orders * 100).round(1)
avg_delay       = df[df['Is Late']==1]['Shipping Delay Days'].mean().round(1)
total_sales     = df['Sales'].sum()
total_profit    = df['Order Profit Per Order'].sum()
avg_profit_rate = df['Order Item Profit Ratio'].mean() * 100

print(f"\n{'='*50}")
print("BASELINE KPIs — DEFINE PHASE (DMAIC)")
print(f"{'='*50}")
print(f"Total Orders:          {total_orders:>10,}")
print(f"Late Orders:           {late_orders:>10,}")
print(f"On-Time Delivery Rate: {on_time_rate:>9}%")
print(f"Avg Delay (late only): {avg_delay:>9} days")
print(f"Total Sales:           ${total_sales:>10,.0f}")
print(f"Total Profit:          ${total_profit:>10,.0f}")
print(f"Avg Profit Margin:     {avg_profit_rate:>9.1f}%")
print(f"{'='*50}")

# ── ANALYSIS 1 — Late delivery by region ────────────────────────
print("\nAnalysis 1: Late delivery by region...")
region_late = (
    df.groupby('Order Region')
    .agg(
        Total_Orders=('Order Id', 'count'),
        Late_Orders=('Is Late', 'sum'),
        Avg_Delay=('Shipping Delay Days', 'mean'),
        Total_Sales=('Sales', 'sum')
    )
    .reset_index()
)
region_late['Late_Rate'] = (
    region_late['Late_Orders'] / region_late['Total_Orders'] * 100
).round(1)
region_late = region_late.sort_values('Late_Rate', ascending=False)

print(region_late[['Order Region','Total_Orders','Late_Rate','Avg_Delay']].to_string(index=False))

fig1 = px.bar(
    region_late,
    x='Late_Rate',
    y='Order Region',
    orientation='h',
    color='Late_Rate',
    color_continuous_scale='Reds',
    title='Late Delivery Rate by Region — Where Are We Failing?',
    labels={'Late_Rate': 'Late Delivery Rate (%)', 'Order Region': 'Region'},
    text='Late_Rate'
)
fig1.update_traces(texttemplate='%{text}%', textposition='outside')
fig1.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
fig1.write_html('outputs/01_late_delivery_by_region.html')
print("Saved: outputs/01_late_delivery_by_region.html")

# ── ANALYSIS 2 — Late delivery by shipping mode ─────────────────
print("\nAnalysis 2: Late delivery by shipping mode...")
ship_late = (
    df.groupby('Shipping Mode')
    .agg(
        Total_Orders=('Order Id', 'count'),
        Late_Orders=('Is Late', 'sum'),
        Avg_Delay=('Shipping Delay Days', 'mean')
    )
    .reset_index()
)
ship_late['Late_Rate'] = (
    ship_late['Late_Orders'] / ship_late['Total_Orders'] * 100
).round(1)

fig2 = px.bar(
    ship_late.sort_values('Late_Rate', ascending=False),
    x='Shipping Mode',
    y='Late_Rate',
    color='Late_Rate',
    color_continuous_scale='Oranges',
    title='Late Delivery Rate by Shipping Mode',
    labels={'Late_Rate': 'Late Delivery Rate (%)', 'Shipping Mode': 'Shipping Mode'},
    text='Late_Rate'
)
fig2.update_traces(texttemplate='%{text}%', textposition='outside')
fig2.update_layout(height=450)
fig2.write_html('outputs/02_late_delivery_by_shipping_mode.html')
print("Saved: outputs/02_late_delivery_by_shipping_mode.html")

# ── ANALYSIS 3 — Revenue and profit by category ─────────────────
print("\nAnalysis 3: Revenue and profit by category...")
cat_revenue = (
    df.groupby('Category Name')
    .agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Order Profit Per Order', 'sum'),
        Total_Orders=('Order Id', 'count'),
        Avg_Profit_Ratio=('Order Item Profit Ratio', 'mean')
    )
    .reset_index()
    .sort_values('Total_Sales', ascending=False)
    .head(15)
)
cat_revenue['Avg_Profit_Ratio'] = (cat_revenue['Avg_Profit_Ratio'] * 100).round(1)

fig3 = px.bar(
    cat_revenue,
    x='Total_Sales',
    y='Category Name',
    orientation='h',
    color='Avg_Profit_Ratio',
    color_continuous_scale='Blues',
    title='Top 15 Categories by Revenue — Color = Profit Margin %',
    labels={
        'Total_Sales': 'Total Sales ($)',
        'Category Name': 'Product Category',
        'Avg_Profit_Ratio': 'Profit Margin %'
    }
)
fig3.update_layout(height=550, yaxis={'categoryorder': 'total ascending'})
fig3.write_html('outputs/03_revenue_by_category.html')
print("Saved: outputs/03_revenue_by_category.html")

# ── ANALYSIS 4 — Customer segment analysis ──────────────────────
print("\nAnalysis 4: Customer segment analysis...")
seg_data = (
    df.groupby('Customer Segment')
    .agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Order Profit Per Order', 'sum'),
        Total_Orders=('Order Id', 'count'),
        Unique_Customers=('Customer Id', 'nunique')
    )
    .reset_index()
)
seg_data['Avg_Order_Value'] = (
    seg_data['Total_Sales'] / seg_data['Total_Orders']
).round(2)

fig4 = px.pie(
    seg_data,
    values='Total_Sales',
    names='Customer Segment',
    title='Revenue Distribution by Customer Segment',
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig4.write_html('outputs/04_customer_segment_revenue.html')
print("Saved: outputs/04_customer_segment_revenue.html")

# ── ANALYSIS 5 — Monthly sales trend ───────────────────────────
print("\nAnalysis 5: Monthly sales trend...")
monthly = (
    df.groupby(['Order Year', 'Order Month', 'Order Month Name'])
    .agg(
        Total_Sales=('Sales', 'sum'),
        Total_Orders=('Order Id', 'count'),
        Late_Rate=('Is Late', 'mean')
    )
    .reset_index()
    .sort_values(['Order Year', 'Order Month'])
)
monthly['Period'] = (monthly['Order Month Name'] + ' ' +
                     monthly['Order Year'].astype(str))
monthly['Late_Rate'] = (monthly['Late_Rate'] * 100).round(1)

fig5 = px.line(
    monthly,
    x='Period',
    y='Total_Sales',
    title='Monthly Sales Trend',
    labels={'Total_Sales': 'Total Sales ($)', 'Period': 'Month'},
    markers=True
)
fig5.update_layout(height=400, xaxis_tickangle=-45)
fig5.write_html('outputs/05_monthly_sales_trend.html')
print("Saved: outputs/05_monthly_sales_trend.html")

# ── ANALYSIS 6 — ABC inventory segmentation ────────────────────
print("\nAnalysis 6: ABC inventory segmentation...")
product_revenue = (
    df.groupby('Product Name')
    .agg(
        Total_Sales=('Sales', 'sum'),
        Total_Orders=('Order Id', 'count'),
        Total_Profit=('Order Profit Per Order', 'sum')
    )
    .reset_index()
    .sort_values('Total_Sales', ascending=False)
)

total_rev = product_revenue['Total_Sales'].sum()
product_revenue['Cumulative_Pct'] = (
    product_revenue['Total_Sales'].cumsum() / total_rev * 100
)
product_revenue['ABC_Class'] = product_revenue['Cumulative_Pct'].apply(
    lambda x: 'A (Top 80%)' if x <= 80 else ('B (80-95%)' if x <= 95 else 'C (Bottom 5%)')
)

abc_summary = product_revenue.groupby('ABC_Class').agg(
    Products=('Product Name', 'count'),
    Total_Sales=('Total_Sales', 'sum')
).reset_index()

fig6 = px.bar(
    abc_summary,
    x='ABC_Class',
    y='Total_Sales',
    color='ABC_Class',
    title='ABC Inventory Segmentation — Revenue by Class',
    labels={'Total_Sales': 'Total Sales ($)', 'ABC_Class': 'Inventory Class'},
    color_discrete_map={
        'A (Top 80%)': '#0F6E56',
        'B (80-95%)': '#185FA5',
        'C (Bottom 5%)': '#A32D2D'
    },
    text='Products'
)
fig6.update_traces(texttemplate='%{text} products', textposition='outside')
fig6.update_layout(height=400)
fig6.write_html('outputs/06_abc_inventory_segmentation.html')
print("Saved: outputs/06_abc_inventory_segmentation.html")

# ── SUMMARY REPORT ──────────────────────────────────────────────
print(f"\n{'='*60}")
print("ANALYSIS COMPLETE — DMAIC SUMMARY")
print(f"{'='*60}")
print(f"DEFINE:   {total_orders:,} orders analyzed across global supply chain")
print(f"MEASURE:  On-time delivery rate: {on_time_rate}% | "
      f"Late orders: {late_orders:,}")
print(f"ANALYZE:  Worst region: {region_late.iloc[0]['Order Region']} "
      f"({region_late.iloc[0]['Late_Rate']}% late rate)")
print(f"ANALYZE:  Best region:  {region_late.iloc[-1]['Order Region']} "
      f"({region_late.iloc[-1]['Late_Rate']}% late rate)")
print(f"IMPROVE:  Focus recruitment + logistics on worst performing regions")
print(f"CONTROL:  Live dashboard monitors KPIs in real time")
print(f"{'='*60}")
print(f"\nTotal Revenue Analyzed: ${total_sales:,.0f}")
print(f"Total Profit Analyzed:  ${total_profit:,.0f}")
print(f"\n6 output files saved in outputs/ folder")
print("Open each .html file in your browser to see charts")