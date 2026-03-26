import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

st.title("🛍️ Retail Sales & Product Dashboard")
st.markdown("This dashboard provides an overview of the retail sales data, highlighting key performance metrics, product category distributions, and sales trends.")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    product_df = pd.read_csv('product_master.csv')
    sales_df = pd.read_csv('sales_transactions.csv')
    
    # Clean data
    sales_df['order_date'] = pd.to_datetime(sales_df['order_date'], format='%d-%m-%Y')
    sales_df['discount_pct'] = sales_df['discount_pct'].str.replace('%', '').astype(float) / 100
    
    # Merge data
    master_df = pd.merge(sales_df, product_df, on='product_id', how='left')
    master_df['revenue'] = master_df['quantity'] * master_df['unit_price'] * (1 - master_df['discount_pct'])
    
    return product_df, sales_df, master_df

try:
    product_df, sales_df, master_df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")

# Date Filter
min_date = master_df['order_date'].min().date()
max_date = master_df['order_date'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Category Filter
categories = ["All"] + sorted(list(master_df['category'].dropna().unique()))
selected_category = st.sidebar.selectbox("Select Category", categories, index=0)

# Region Filter
regions = ["All"] + sorted(list(master_df['region'].dropna().unique()))
selected_region = st.sidebar.selectbox("Select Region", regions, index=0)

# --- APPLY FILTERS ---
date_filtered = master_df[
    (master_df['order_date'].dt.date >= start_date) & 
    (master_df['order_date'].dt.date <= end_date)
]

if selected_category != "All":
    date_filtered = date_filtered[date_filtered['category'] == selected_category]
    
if selected_region != "All":
    date_filtered = date_filtered[date_filtered['region'] == selected_region]
    
filtered_df = date_filtered

# --- KPI METRICS ---
st.markdown("---")
st.subheader("Key Performance Indicators (KPIs)")

if not filtered_df.empty:
    total_rev = filtered_df['revenue'].sum()
    total_ords = len(filtered_df)
    avg_ord_val = filtered_df['revenue'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${total_rev:,.2f}")
    col2.metric("Total Orders", f"{total_ords:,}")
    col3.metric("Average Order Value", f"${avg_ord_val:,.2f}")
    
    top_cat = filtered_df.groupby('category')['revenue'].sum().idxmax() if not filtered_df.empty else "N/A"
    col4.metric("Top Category", top_cat)
else:
    st.warning("No data matches the selected filters.")

st.markdown("---")

# --- CHARTS ---
if not filtered_df.empty:
    col_chart1, col_chart2 = st.columns(2)
    
    sns.set_theme(style="whitegrid")
    
    # Chart 1: Revenue by Category
    with col_chart1:
        st.subheader("Revenue by Product Category")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        cat_sales = filtered_df.groupby('category')['revenue'].sum().sort_values(ascending=False).reset_index()
        sns.barplot(data=cat_sales, x='category', y='revenue', palette='viridis', ax=ax1)
        plt.xticks(rotation=45)
        plt.xlabel("")
        plt.ylabel("Revenue ($)")
        st.pyplot(fig1)

    # Chart 2: Revenue Trend over Time
    with col_chart2:
        st.subheader("Monthly Sales Revenue Trend")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        monthly_sales = filtered_df.groupby(filtered_df['order_date'].dt.to_period('M'))['revenue'].sum().reset_index()
        monthly_sales['order_date'] = monthly_sales['order_date'].dt.to_timestamp()
        sns.lineplot(data=monthly_sales, x='order_date', y='revenue', marker='o', color='crimson', ax=ax2)
        plt.xticks(rotation=45)
        plt.xlabel("")
        plt.ylabel("Revenue ($)")
        st.pyplot(fig2)

    # Chart 3: Order Quantity Distribution
    st.subheader("Distribution of Order Quantities")
    fig3, ax3 = plt.subplots(figsize=(10, 3))
    sns.histplot(filtered_df['quantity'], bins=range(1, int(filtered_df['quantity'].max()) + 2), kde=False, color='teal', ax=ax3)
    plt.xlabel("Quantity Purchased per Order")
    plt.ylabel("Number of Orders")
    st.pyplot(fig3)

# --- RAW DATA ---
st.markdown("---")
st.subheader("Raw Data Preview")
with st.expander("Show Master Dataset (Filtered)"):
    st.dataframe(filtered_df.head(100), use_container_width=True)
    st.caption("Showing up to 100 rows based on current filters.")
