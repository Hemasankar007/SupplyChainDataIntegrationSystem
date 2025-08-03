import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

class LogisticsDashboard:
    def __init__(self):
        st.set_page_config(page_title="Logistics Intelligence Dashboard", page_icon="📦", layout="wide")
        st.markdown("""
    <style>
        .stApp {
            background-color: #ff4d4d;
        }
    </style>
""", unsafe_allow_html=True)
        

        self.sidebar_menu()

    def sidebar_menu(self):
        st.sidebar.title("📦 Logistics Menu")
        option = st.sidebar.radio(
            "Select View",
            ["Summary", "Shipments", "Warehouse", "Returns", "Insights", "Export Data"]
        )
        if option == "Summary":
            self.show_summary()
        elif option == "Shipments":
            self.show_shipments()
        elif option == "Warehouse":
            self.show_warehouse()
        elif option == "Returns":
            self.show_returns()
        elif option == "Insights":
            self.show_insights()
        elif option == "Export Data":
            self.export_data()

    def show_summary(self):
        st.title("🚛 Logistics Summary")
        st.markdown("Explore a quick snapshot of logistics operations.")
        st.image("https://images.unsplash.com/photo-1581091012184-df4bd7f1b3b9", use_container_width=True)
        st.success("Welcome to the Logistics Intelligence Dashboard!")

    def show_shipments(self):
        st.header("📦 Shipment Records")
        df = self.load_shipments()
        st.dataframe(df)
        st.line_chart(df["Freight Cost"])

    def show_warehouse(self):
        st.header("🏢 Warehouse Stock")
        df = self.load_warehouse()
        st.dataframe(df)
        st.area_chart(df["Stock Count"])

    def show_returns(self):
        st.header("🔄 Return Records")
        df = self.load_returns()
        st.dataframe(df)

    def show_insights(self):
        st.header("📈 Operational Insights")
        shipments = self.load_shipments()
        warehouse = self.load_warehouse()
        st.subheader("Freight Time Spread")
        st.bar_chart(shipments["Freight Time (days)"])
        st.subheader("Low Inventory Alerts")
        st.write(f"Items below threshold: {warehouse['Low Stock'].sum()}")

    def export_data(self):
        st.header("📤 Export Shipments Data")
        df = self.load_shipments()
        csv = df.to_csv(index=False)
        st.download_button("Download Shipment CSV", csv, "shipments.csv", "text/csv")

    def show_analytics(self):
        st.header("📊 Supply Chain Analytics")
        orders = self.get_sample_orders()
        inventory = self.get_sample_inventory()
        returns = self.get_sample_returns()

        # Lead Time Metrics
        avg_lead_time = orders["Lead Time (Days)"].mean()
        st.metric("Average Lead Time (Days)", f"{avg_lead_time:.2f}")

        # Return Rate
        total_orders = len(orders)
        total_returns = len(returns)
        return_rate = (total_returns / total_orders) * 100 if total_orders else 0
        st.metric("Return Rate (%)", f"{return_rate:.2f}")

        # Inventory Stockout Risk
        stockout_count = inventory["stockout_risk"].sum()
        st.metric("Products at Stockout Risk", stockout_count)

        # Sales Metrics
        total_sales = orders["Sales"].sum()
        avg_sales = orders["Sales"].mean()
        st.metric("Total Sales", f"${total_sales:,.2f}")
        st.metric("Average Sales per Order", f"${avg_sales:,.2f}")

        # Visualizations
        st.subheader("Lead Time Distribution")
        st.bar_chart(orders["Lead Time (Days)"])

        st.subheader("Sales Over Time")
        st.line_chart(orders.set_index("Order Date")["Sales"])

        st.subheader("Stock Levels")
        st.area_chart(inventory["stock_level"])

        st.subheader("Return Events")
        st.dataframe(returns)

    # Sample data methods
    def load_shipments(self):
        return pd.DataFrame({
            'Shipment ID': [f'SHP_{i}' for i in range(1, 16)],
            'Freight Cost': np.random.uniform(50, 500, 15),
            'Freight Time (days)': np.random.randint(2, 10, 15),
            'Shipment Date': pd.date_range('2024-02-01', periods=15, freq='D')
        })

    def load_warehouse(self):
        return pd.DataFrame({
            'Item ID': [f'ITEM_{i}' for i in range(1, 15)],
            'Stock Count': np.random.randint(5, 150, 14),
            'Low Stock': np.random.choice([True, False], 14, p=[0.3, 0.7])
        })

    def load_returns(self):
        return pd.DataFrame({
            'Return ID': [f'RTN_{i}' for i in range(1, 6)],
            'Return Date': pd.date_range('2024-02-01', periods=5, freq='D'),
            'Shipment ID': [f'SHP_{i}' for i in np.random.randint(1, 15, 5)]
        })

    def get_sample_orders(self):
        return pd.DataFrame({
            'Order ID': [f'ORD_{i}' for i in range(1, 21)],
            'Sales': np.random.uniform(10, 1000, 20),
            'Order Date': pd.date_range('2024-01-01', periods=20, freq='D'),
            'Lead Time (Days)': np.random.randint(1, 15, 20)
        })

    def get_sample_inventory(self):
        return pd.DataFrame({
            'Item ID': [f'ITEM_{i}' for i in range(1, 21)],
            'stock_level': np.random.randint(0, 200, 20),
            'stockout_risk': np.random.choice([True, False], 20, p=[0.2, 0.8])
        })

    def get_sample_returns(self):
        return pd.DataFrame({
            'Return ID': [f'RTN_{i}' for i in range(1, 11)],
            'Order ID': [f'ORD_{i}' for i in np.random.randint(1, 21, 10)],
            'Return Date': pd.date_range('2024-01-01', periods=10, freq='D')
        })

def main():
    LogisticsDashboard()

if __name__ == "__main__":
    main()
