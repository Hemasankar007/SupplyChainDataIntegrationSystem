import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

class SupplyChainDashboard:
    def __init__(self):
        st.set_page_config(page_title="Supply Chain Dashboard", page_icon="🚚", layout="wide")
        self.sidebar_navigation()

    def sidebar_navigation(self):
        st.sidebar.title("🚚 Supply Chain Navigation")
        page = st.sidebar.radio(
            "Go to",
            ["Overview", "Orders", "Inventory", "Returns", "Analytics", "Download Report"]
        )
        if page == "Overview":
            self.show_overview()
        elif page == "Orders":
            self.show_orders()
        elif page == "Inventory":
            self.show_inventory()
        elif page == "Returns":
            self.show_returns()
        elif page == "Analytics":
            self.show_analytics()
        elif page == "Download Report":
            self.download_report()

    def show_overview(self):
        st.title("📦 Supply Chain Overview")
        st.markdown("""
        Welcome to your **personalized logistics analytics dashboard**!  
        This platform empowers you to monitor and optimize every stage of your supply chain with clarity and precision.

        🚚 **What you can do here:**
        - Track **order performance** and visualize trends over time  
        - Monitor **inventory health** and spot potential stockouts  
        - Analyze **product returns** and identify causes  
        - Get real-time **analytics** on lead times, stock levels, and more  
        - Download custom **reports** for deeper analysis or sharing  

        Stay informed, make data-driven decisions, and elevate operational efficiency across your supply chain.
        """)
        st.image("https://images.unsplash.com/photo-1515165562835-cf7747d3b6b5", use_container_width=True)
        st.info("This dashboard provides a modern interface for supply chain analytics.")

    def show_orders(self):
        st.header("📝 Orders Data")
        orders = self.get_sample_orders()
        st.dataframe(orders)
        st.bar_chart(orders["Sales"])

    def show_inventory(self):
        st.header("🏬 Inventory Data")
        inventory = self.get_sample_inventory()
        st.dataframe(inventory)
        st.line_chart(inventory["stock_level"])

    def show_returns(self):
        st.header("↩️ Returns Data")
        returns = self.get_sample_returns()
        st.dataframe(returns)

    def show_analytics(self):
        st.header("📊 Analytics")
        orders = self.get_sample_orders()
        inventory = self.get_sample_inventory()
        st.subheader("Order Lead Time Distribution")
        st.bar_chart(orders["Lead Time (Days)"])
        st.subheader("Inventory Stockout Risk")
        st.write(f"Products at risk: {inventory['stockout_risk'].sum()}")

    def download_report(self):
        st.header("⬇️ Download Report")
        orders = self.get_sample_orders()
        csv = orders.to_csv(index=False)
        st.download_button("Download Orders CSV", csv, "orders.csv", "text/csv")

    def get_sample_orders(self):
        return pd.DataFrame({
            'Order ID': [f'ORD_{i}' for i in range(1, 21)],
            'Order Date': pd.date_range('2024-01-01', periods=20, freq='D'),
            'Sales': np.random.uniform(100, 1000, 20),
            'Lead Time (Days)': np.random.randint(1, 15, 20)
        })

    def get_sample_inventory(self):
        return pd.DataFrame({
            'product_id': [f'PROD_{i}' for i in range(1, 21)],
            'stock_level': np.random.randint(10, 200, 20),
            'stockout_risk': np.random.choice([True, False], 20, p=[0.2, 0.8])
        })

    def get_sample_returns(self):
        return pd.DataFrame({
            'Return Date': pd.date_range('2024-01-01', periods=5, freq='D'),
            'Order ID': [f'ORD_{i}' for i in np.random.randint(1, 21, 5)]
        })

def main():
    SupplyChainDashboard()

if __name__ == "__main__":
    main()
