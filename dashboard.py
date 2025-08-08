import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Helper function to generate sample data
def load_sample_data():
    num_orders = 200
    num_inventory_records = 500
    start_date = datetime(2023, 1, 1)

    # Sample Orders Data
    orders_df = pd.DataFrame({
        'Order ID': [f'ORD_{i:03d}' for i in range(1, num_orders + 1)],
        'Order Date': pd.to_datetime([start_date + timedelta(days=np.random.randint(0, 364)) for _ in range(num_orders)]),
        'Customer ID': [f'CUST_{i%30:02d}' for i in range(1, num_orders + 1)],
        'Product ID': [f'PROD_{i%20:02d}' for i in range(1, num_orders + 1)],
        'Category': np.random.choice(['Electronics', 'Apparel', 'Home Goods', 'Groceries', 'Books'], num_orders),
        'Quantity': np.random.randint(1, 8, num_orders),
        'Sales': np.random.uniform(50, 1200, num_orders),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], num_orders)
    })
    orders_df['Ship Date'] = orders_df['Order Date'] + pd.to_timedelta(np.random.randint(1, 5, num_orders), unit='d')
    orders_df['Lead Time (Days)'] = (orders_df['Ship Date'] - orders_df['Order Date']).dt.days

    # Sample Inventory Data
    inventory_df = pd.DataFrame({
        'date': pd.to_datetime([start_date + timedelta(days=np.random.randint(0, 364)) for _ in range(num_inventory_records)]),
        'product_id': [f'PROD_{i%20:02d}' for i in range(num_inventory_records)],
        'category': np.random.choice(['Electronics', 'Apparel', 'Home Goods', 'Groceries', 'Books'], num_inventory_records),
        'stock_level': np.random.randint(20, 250, num_inventory_records),
        'daily_demand': np.random.randint(5, 25, num_inventory_records),
    })
    inventory_df['fill_rate'] = np.random.uniform(0.90, 0.99, num_inventory_records)
    inventory_df['annualized_turnover'] = (inventory_df['daily_demand'] * 365) / inventory_df['stock_level']
    inventory_df['stockout_risk'] = inventory_df['fill_rate'] < 0.5

    return orders_df, inventory_df

# Main function for the Streamlit app
def main():
    st.set_page_config(
        page_title="Enhanced Supply Chain Dashboard",
        page_icon="🚀",
        layout="wide"
    )

    # Load data
    orders_df, inventory_df = load_sample_data()

    # Sidebar for filters
    st.sidebar.title("Filters")
    date_range = st.sidebar.date_input("Select Date Range", [orders_df['Order Date'].min(), orders_df['Order Date'].max()])
    start_date, end_date = pd.to_datetime(date_range)

    selected_categories = st.sidebar.multiselect("Filter by Category", orders_df['Category'].unique(), default=orders_df['Category'].unique())
    selected_regions = st.sidebar.multiselect("Filter by Region", orders_df['Region'].unique(), default=orders_df['Region'].unique())
    # If no categories are selected, include all categories
    category_filter = orders_df['Category'].isin(selected_categories) if selected_categories else True
    # If no regions are selected, include all regions
    region_filter = orders_df['Region'].isin(selected_regions) if selected_regions else True

    filtered_orders = orders_df[
        (orders_df['Order Date'] >= start_date) & (orders_df['Order Date'] <= end_date) &
        category_filter & region_filter
    ]

    # If no categories are selected, include all categories for inventory
    inventory_category_filter = inventory_df['category'].isin(selected_categories) if selected_categories else True

    filtered_inventory = inventory_df[
        (inventory_df['date'] >= start_date) & (inventory_df['date'] <= end_date) &
        inventory_category_filter
    ]

    # Main dashboard title
    st.title("🚀 Enhanced Supply Chain Analytics Dashboard")
    st.markdown("An interactive dashboard for monitoring key supply chain metrics.")

    # KPI Scorecards
    st.header("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sales", f"₹{filtered_orders['Sales'].sum():,.2f}")
    with col2:
        st.metric("Total Orders", f"{len(filtered_orders):,}")
    with col3:
        st.metric("Avg. Lead Time", f"{filtered_orders['Lead Time (Days)'].mean():.2f} Days")
    with col4:
        st.metric("Avg. Fill Rate", f"{filtered_inventory['fill_rate'].mean():.2%}")

    # Charts and Visualizations
    st.header("Visualizations")
    
    # Sales Trend
    sales_trend = filtered_orders.groupby(pd.Grouper(key='Order Date', freq='M'))['Sales'].sum().reset_index()
    fig_sales = px.line(sales_trend, x='Order Date', y='Sales', title='Monthly Sales Trend', markers=True)
    st.plotly_chart(fig_sales, use_container_width=True)

    # Sales Analysis with Radio Buttons
    st.subheader("Sales Breakdown")
    sales_breakdown_option = st.radio(
        "View Sales By:",
        ("Category", "Region"),
        horizontal=True
    )

    if sales_breakdown_option == "Category":
        category_sales = filtered_orders.groupby('Category')['Sales'].sum().reset_index()
        fig_category = px.bar(category_sales, x='Category', y='Sales', title='Sales by Category', text_auto=True)
        fig_category.update_layout(xaxis_title="Product Category", yaxis_title="Total Sales (₹)")
        st.plotly_chart(fig_category, use_container_width=True)
    elif sales_breakdown_option == "Region":
        regional_sales = filtered_orders.groupby('Region')['Sales'].sum().reset_index()
        fig_regional = px.pie(regional_sales, names='Region', values='Sales', title='Sales by Region', hole=0.4)
        fig_regional.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_regional, use_container_width=True)

    # Inventory Analysis
    inventory_trend = filtered_inventory.groupby(pd.Grouper(key='date', freq='M'))['stock_level'].mean().reset_index()
    fig_inventory = px.area(inventory_trend, x='date', y='stock_level', title='Average Stock Level Over Time')
    st.plotly_chart(fig_inventory, use_container_width=True)

    # Data Table
    st.header("Detailed Order Data")
    st.dataframe(filtered_orders)

    # Export functionality
    st.sidebar.title("Export Data")
    if st.sidebar.button("Export to CSV"):
        csv = filtered_orders.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name='filtered_orders.csv',
            mime='text/csv',
        )
        st.sidebar.success("Exported successfully!")

if __name__ == "__main__":
    main()