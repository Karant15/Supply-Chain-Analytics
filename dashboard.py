import pandas as pd
import plotly.express as px
import streamlit as st
import warnings
import os
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Supply Chain Analytics",
    page_icon="🚚",
    layout="wide"
)

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Karant15/Supply-Chain-Analytics/master/data/supply_chain_sample.csv"
    df = pd.read_csv(url, encoding='latin-1')
    df['order date (DateOrders)'] = pd.to_datetime(
        df['order date (DateOrders)'], errors='coerce'
    )
    df['Order Year']  = df['order date (DateOrders)'].dt.year
    df['Order Month'] = df['order date (DateOrders)'].dt.month
    df['Order Month Name'] = df['order date (DateOrders)'].dt.strftime('%b')
    df['Is Late'] = (df['Days for shipping (real)'] >
                     df['Days for shipment (scheduled)']).astype(int)
    df['Shipping Delay Days'] = (df['Days for shipping (real)'] -
                                  df['Days for shipment (scheduled)'])
    return df

# ── HEADER ──────────────────────────────────────────────────────
st.title("🚚 Supply Chain Analytics Dashboard")
st.markdown("**Real DataCo Supply Chain Data — 180,519 Orders | Global Markets | 2015–2018**")
st.markdown("*Identifying delivery failures, revenue gaps, and inventory priorities using Lean Six Sigma DMAIC*")
st.divider()

with st.spinner("Loading 180,519 supply chain orders..."):
    df = load_data()

# ── SIDEBAR FILTERS ─────────────────────────────────────────────
st.sidebar.header("🔍 Filters")
all_regions  = sorted(df['Order Region'].dropna().unique())
all_segments = sorted(df['Customer Segment'].dropna().unique())
all_modes    = sorted(df['Shipping Mode'].dropna().unique())
all_years    = sorted(df['Order Year'].dropna().unique())

selected_regions  = st.sidebar.multiselect("Regions", all_regions, default=all_regions)
selected_segments = st.sidebar.multiselect("Customer Segments", all_segments, default=all_segments)
selected_modes    = st.sidebar.multiselect("Shipping Mode", all_modes, default=all_modes)
selected_years    = st.sidebar.multiselect("Year", all_years, default=all_years)

dff = df.copy()
if selected_regions:  dff = dff[dff['Order Region'].isin(selected_regions)]
if selected_segments: dff = dff[dff['Customer Segment'].isin(selected_segments)]
if selected_modes:    dff = dff[dff['Shipping Mode'].isin(selected_modes)]
if selected_years:    dff = dff[dff['Order Year'].isin(selected_years)]

# ── TOP KPIs ────────────────────────────────────────────────────
total_orders   = len(dff)
late_orders    = dff['Is Late'].sum()
on_time_rate   = round((total_orders - late_orders) / total_orders * 100, 1) if total_orders > 0 else 0
total_sales    = dff['Sales'].sum()
total_profit   = dff['Order Profit Per Order'].sum()
avg_margin     = dff['Order Item Profit Ratio'].mean() * 100

c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("Total Orders",     f"{total_orders:,}")
c2.metric("Late Orders",      f"{late_orders:,}")
c3.metric("On-Time Rate",     f"{on_time_rate}%",
          delta=f"{on_time_rate - 57.3:.1f}% vs baseline")
c4.metric("Total Sales",      f"${total_sales:,.0f}")
c5.metric("Total Profit",     f"${total_profit:,.0f}")
c6.metric("Avg Profit Margin",f"{avg_margin:.1f}%")
st.divider()

# ── TABS ────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5 = st.tabs([
    "📊 Executive Summary",
    "🚨 Delivery Performance",
    "💰 Revenue & Profit",
    "📦 Inventory ABC",
    "📋 DMAIC Report"
])

# ── TAB 1: EXECUTIVE SUMMARY ────────────────────────────────────
with tab1:
    st.subheader("Executive Summary")
    st.markdown("> **Key Finding:** Only **42.7%** of orders are delivered on time globally. "
                "Central Africa has the worst late delivery rate at **60.7%**. "
                "Immediate action required on shipping mode optimization.")

    col1, col2 = st.columns(2)
    with col1:
        region_late = (
            dff.groupby('Order Region')
            .agg(Total_Orders=('Order Id','count'), Late_Orders=('Is Late','sum'))
            .reset_index()
        )
        region_late['Late_Rate'] = (
            region_late['Late_Orders'] / region_late['Total_Orders'] * 100
        ).round(1)
        region_late = region_late.sort_values('Late_Rate', ascending=False)
        fig = px.bar(
            region_late,
            x='Late_Rate', y='Order Region', orientation='h',
            color='Late_Rate', color_continuous_scale='Reds',
            title='Late Delivery Rate by Region (%)',
            labels={'Late_Rate':'Late Rate (%)','Order Region':'Region'},
            text='Late_Rate'
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        ship_perf = (
            dff.groupby('Shipping Mode')
            .agg(Total_Orders=('Order Id','count'), Late_Orders=('Is Late','sum'))
            .reset_index()
        )
        ship_perf['Late_Rate'] = (
            ship_perf['Late_Orders'] / ship_perf['Total_Orders'] * 100
        ).round(1)
        fig2 = px.bar(
            ship_perf.sort_values('Late_Rate', ascending=False),
            x='Shipping Mode', y='Late_Rate',
            color='Late_Rate', color_continuous_scale='Oranges',
            title='Late Delivery Rate by Shipping Mode (%)',
            labels={'Late_Rate':'Late Rate (%)'},
            text='Late_Rate'
        )
        fig2.update_traces(texttemplate='%{text}%', textposition='outside')
        fig2.update_layout(height=500)
        st.plotly_chart(fig2, use_container_width=True)

# ── TAB 2: DELIVERY PERFORMANCE ─────────────────────────────────
with tab2:
    st.subheader("🚨 Delivery Performance Analysis")
    st.markdown("**DMAIC — Measure Phase:** Quantifying the delivery failure problem")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Late Delivery Rate by Region")
        st.dataframe(
            region_late[['Order Region','Total_Orders','Late_Orders','Late_Rate']]
            .rename(columns={
                'Order Region':'Region',
                'Total_Orders':'Total Orders',
                'Late_Orders':'Late Orders',
                'Late_Rate':'Late Rate (%)'
            }),
            hide_index=True, use_container_width=True
        )

    with col2:
        delivery_dist = dff['Delivery Status'].value_counts().reset_index()
        delivery_dist.columns = ['Status','Count']
        fig3 = px.pie(
            delivery_dist, values='Count', names='Status',
            title='Order Delivery Status Distribution',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("##### Shipping Delay Distribution")
    delay_data = dff[dff['Is Late']==1]['Shipping Delay Days']
    fig4 = px.histogram(
        delay_data, nbins=20,
        title='Distribution of Shipping Delays (Late Orders Only)',
        labels={'value':'Delay Days','count':'Number of Orders'},
        color_discrete_sequence=['#A32D2D']
    )
    fig4.update_layout(height=350)
    st.plotly_chart(fig4, use_container_width=True)

# ── TAB 3: REVENUE & PROFIT ─────────────────────────────────────
with tab3:
    st.subheader("💰 Revenue & Profit Analysis")

    col1, col2 = st.columns(2)
    with col1:
        cat_rev = (
            dff.groupby('Category Name')
            .agg(Total_Sales=('Sales','sum'), Total_Profit=('Order Profit Per Order','sum'))
            .reset_index()
            .sort_values('Total_Sales', ascending=False)
            .head(15)
        )
        fig5 = px.bar(
            cat_rev, x='Total_Sales', y='Category Name', orientation='h',
            color='Total_Profit', color_continuous_scale='Blues',
            title='Top 15 Categories by Revenue',
            labels={'Total_Sales':'Total Sales ($)','Category Name':'Category',
                    'Total_Profit':'Total Profit ($)'}
        )
        fig5.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        seg_data = (
            dff.groupby('Customer Segment')
            .agg(Total_Sales=('Sales','sum'), Total_Orders=('Order Id','count'))
            .reset_index()
        )
        fig6 = px.pie(
            seg_data, values='Total_Sales', names='Customer Segment',
            title='Revenue by Customer Segment', hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig6, use_container_width=True)

    monthly = (
        dff.groupby(['Order Year','Order Month','Order Month Name'])
        .agg(Total_Sales=('Sales','sum'), Total_Orders=('Order Id','count'))
        .reset_index()
        .sort_values(['Order Year','Order Month'])
    )
    monthly['Period'] = (monthly['Order Month Name'] + ' ' +
                         monthly['Order Year'].astype(str))
    fig7 = px.line(
        monthly, x='Period', y='Total_Sales',
        title='Monthly Sales Trend',
        labels={'Total_Sales':'Total Sales ($)','Period':'Month'},
        markers=True, color_discrete_sequence=['#0F6E56']
    )
    fig7.update_layout(height=380, xaxis_tickangle=-45)
    st.plotly_chart(fig7, use_container_width=True)

# ── TAB 4: ABC INVENTORY ────────────────────────────────────────
with tab4:
    st.subheader("📦 ABC Inventory Segmentation")
    st.markdown("""
    **How to read this:**
    - **Class A** — Top products generating 80% of revenue — protect stock at all costs
    - **Class B** — Mid-tier products generating next 15% — monitor closely
    - **Class C** — Long tail products generating bottom 5% — consider reducing
    """)

    prod_rev = (
        dff.groupby('Product Name')
        .agg(Total_Sales=('Sales','sum'), Total_Orders=('Order Id','count'),
             Total_Profit=('Order Profit Per Order','sum'))
        .reset_index()
        .sort_values('Total_Sales', ascending=False)
    )
    total_rev = prod_rev['Total_Sales'].sum()
    prod_rev['Cumulative_Pct'] = prod_rev['Total_Sales'].cumsum() / total_rev * 100
    prod_rev['ABC_Class'] = prod_rev['Cumulative_Pct'].apply(
        lambda x: 'A — Top 80%' if x <= 80 else ('B — 80-95%' if x <= 95 else 'C — Bottom 5%')
    )

    abc_sum = prod_rev.groupby('ABC_Class').agg(
        Products=('Product Name','count'),
        Total_Sales=('Total_Sales','sum'),
        Total_Profit=('Total_Profit','sum')
    ).reset_index()

    col1, col2 = st.columns(2)
    with col1:
        fig8 = px.bar(
            abc_sum, x='ABC_Class', y='Total_Sales',
            color='ABC_Class', title='Revenue by ABC Class',
            labels={'Total_Sales':'Total Sales ($)','ABC_Class':'Class'},
            color_discrete_map={
                'A — Top 80%':'#0F6E56',
                'B — 80-95%':'#185FA5',
                'C — Bottom 5%':'#A32D2D'
            }, text='Products'
        )
        fig8.update_traces(texttemplate='%{text} products', textposition='outside')
        fig8.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig8, use_container_width=True)

    with col2:
        st.markdown("**ABC Class Summary**")
        st.dataframe(
            abc_sum.rename(columns={
                'ABC_Class':'Class','Products':'# Products',
                'Total_Sales':'Total Sales ($)','Total_Profit':'Total Profit ($)'
            }),
            hide_index=True, use_container_width=True
        )
        st.markdown("**Top 10 Class A Products**")
        st.dataframe(
            prod_rev[prod_rev['ABC_Class']=='A — Top 80%']
            [['Product Name','Total_Sales','Total_Orders']]
            .head(10)
            .rename(columns={'Product Name':'Product',
                             'Total_Sales':'Sales ($)',
                             'Total_Orders':'Orders'}),
            hide_index=True, use_container_width=True
        )

# ── TAB 5: DMAIC REPORT ─────────────────────────────────────────
with tab5:
    st.subheader("📋 DMAIC Six Sigma Report")
    st.markdown("*Lean Six Sigma Black Belt framework applied to supply chain gap analysis*")

    st.markdown("### 🎯 DEFINE — Problem Statement")
    st.info("""
    **Business Problem:** Only 42.7% of global supply chain orders are delivered on time,
    resulting in customer dissatisfaction, potential revenue loss, and competitive disadvantage.

    **Goal:** Identify root causes of late deliveries and recommend targeted interventions
    to improve on-time delivery rate to 70%+ within 6 months.

    **Scope:** 180,519 orders across 23 global regions (2015–2018)
    """)

    st.markdown("### 📏 MEASURE — Baseline KPIs")
    kpi_data = {
        'KPI': ['On-Time Delivery Rate','Late Orders','Total Orders Analyzed',
                'Worst Region','Best Region','Total Revenue','Avg Profit Margin'],
        'Baseline Value': ['42.7%','103,400','180,519',
                           'Central Africa (60.7% late)','Canada (51.9% late)',
                           '$36,784,735','12.1%'],
        'Target': ['70%+','< 54,000','—','< 50% late rate','Maintain','Growth','15%+']
    }
    st.dataframe(pd.DataFrame(kpi_data), hide_index=True, use_container_width=True)

    st.markdown("### 🔍 ANALYZE — Root Causes")
    st.warning("""
    **Root Cause 1:** First Class shipping has highest late rate —
    premium customers receiving worst service

    **Root Cause 2:** Central Africa and Western Europe have highest late rates —
    regional logistics partners underperforming

    **Root Cause 3:** Class C inventory products consuming logistics bandwidth
    without contributing proportional revenue
    """)

    st.markdown("### ✅ IMPROVE — Recommendations")
    st.success("""
    **Recommendation 1:** Audit First Class shipping carrier contracts —
    SLA enforcement or carrier switch

    **Recommendation 2:** Regional logistics partner review for Central Africa
    and Western Europe — performance improvement plans

    **Recommendation 3:** Reduce Class C product SKUs by 30% to free up
    warehouse and logistics capacity for Class A products

    **Recommendation 4:** Implement real-time delivery tracking dashboard
    (this dashboard) for ongoing monitoring
    """)

    st.markdown("### 🎛️ CONTROL — Monitoring")
    st.info("""
    **This dashboard serves as the Control phase tool.**
    Use the sidebar filters to monitor KPIs by region, segment, shipping mode,
    and year. Set monthly review cadence with logistics team.
    """)

# ── FOOTER ──────────────────────────────────────────────────────
st.divider()
st.markdown("""
**Data Source:** DataCo Smart Supply Chain Dataset (Mendeley Data)
| **Built by:** Karan Trivedi | MS Data Analytics, Webster University
| **Framework:** Lean Six Sigma DMAIC | **Tools:** Python · Plotly · Streamlit
""")