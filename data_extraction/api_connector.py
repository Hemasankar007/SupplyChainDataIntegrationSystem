import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from utils.logger import log_pipeline_step, log_data_quality_check
from config import FAKE_STORE_API_BASE_URL, INVENTORY_SIMULATION_DAYS, RESTOCKING_FREQUENCY, DEMAND_VARIABILITY

class ExternalAPIHandler:
    """
    Manages API interaction and inventory forecasting logic
    """

    def __init__(self):
        self.logger = log_pipeline_step("ExternalAPIHandler", "INITIATED")
        self.base_url = FAKE_STORE_API_BASE_URL

    def fetch_products(self):
        """
        Retrieve product data from the external Fake Store API
        """
        try:
            self.logger.info("Requesting product list from API...")
            response = requests.get(f"{self.base_url}/products")
            response.raise_for_status()
            product_data = pd.DataFrame(response.json())
            self._validate_product_data(product_data)
            self.logger.info(f"Successfully fetched {len(product_data)} products.")
            return product_data
        except Exception as e:
            self.logger.error(f"Failed to fetch products: {str(e)}")
            return None

    def fetch_categories(self):
        """
        Retrieve product categories from the Fake Store API
        """
        try:
            self.logger.info("Requesting product categories from API...")
            response = requests.get(f"{self.base_url}/products/categories")
            response.raise_for_status()
            categories_df = pd.DataFrame(response.json(), columns=['category'])
            self.logger.info(f"Fetched {len(categories_df)} categories successfully.")
            return categories_df
        except Exception as e:
            self.logger.error(f"Failed to fetch categories: {str(e)}")
            return None

    def simulate_inventory_activity(self, product_df, simulation_days=INVENTORY_SIMULATION_DAYS):
        """
        Generate synthetic inventory records over a defined timeframe
        """
        try:
            self.logger.info(f"Simulating inventory for {simulation_days} days...")
            inventory_records = []
            simulation_start = datetime.now() - timedelta(days=simulation_days)

            for day in range(simulation_days):
                simulation_date = simulation_start + timedelta(days=day)

                for _, item in product_df.iterrows():
                    base_demand = random.randint(1, 10)
                    adjusted_demand = max(0, int(base_demand * random.uniform(1 - DEMAND_VARIABILITY, 1 + DEMAND_VARIABILITY)))

                    if day == 0:
                        stock_today = random.randint(50, 200)
                    else:
                        prev_entry = next((r for r in inventory_records if r['product_id'] == item['id'] and r['date'] == simulation_date - timedelta(days=1)), None)
                        stock_today = prev_entry['stock_level'] if prev_entry else random.randint(50, 200)

                    current_stock = stock_today - adjusted_demand
                    if day % RESTOCKING_FREQUENCY == 0:
                        restock_qty = random.randint(50, 100)
                        current_stock += restock_qty
                        was_restocked = True
                    else:
                        restock_qty = 0
                        was_restocked = False

                    price_variation = item['price'] * random.uniform(0.95, 1.05)

                    record = {
                        'date': simulation_date,
                        'product_id': item['id'],
                        'product_name': item['title'],
                        'category': item['category'],
                        'daily_demand': adjusted_demand,
                        'stock_level': max(0, current_stock),
                        'restock_amount': restock_qty,
                        'restocked': was_restocked,
                        'price': price_variation,
                        'original_price': item['price'],
                        'price_change_pct': ((price_variation - item['price']) / item['price']) * 100
                    }

                    inventory_records.append(record)

            inventory_df = pd.DataFrame(inventory_records)
            inventory_df = self._append_inventory_metrics(inventory_df)
            self.logger.info(f"Simulation complete. Generated {len(inventory_df)} records.")
            return inventory_df
        except Exception as e:
            self.logger.error(f"Simulation error: {str(e)}")
            return None

    def _validate_product_data(self, df):
        """
        Run product data quality assurance checks
        """
        missing = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        if missing > 0.05:
            log_data_quality_check("Product Null Check", "WARNING", f"{missing:.2%} data missing")
        else:
            log_data_quality_check("Product Null Check", "PASS", f"{missing:.2%} data missing")

        required = ['id', 'title', 'price', 'category']
        missing_cols = [col for col in required if col not in df.columns]
        if missing_cols:
            log_data_quality_check("Product Column Check", "FAIL", f"Missing: {missing_cols}")
        else:
            log_data_quality_check("Product Column Check", "PASS")

        if 'price' in df.columns:
            invalid_price_count = df[df['price'] <= 0].shape[0]
            if invalid_price_count:
                log_data_quality_check("Price Validation", "WARNING", f"Invalid prices: {invalid_price_count}")
            else:
                log_data_quality_check("Price Validation", "PASS")

    def _append_inventory_metrics(self, df):
        """
        Derive advanced inventory insights
        """
        df['days_of_inventory'] = np.where(df['daily_demand'] > 0, df['stock_level'] / df['daily_demand'], np.inf)
        df['stockout_risk'] = df['days_of_inventory'] < 3
        df['annualized_turnover'] = np.where(df['stock_level'] > 0, (df['daily_demand'] * 365) / df['stock_level'], 0)
        df['fill_rate'] = np.where(df['daily_demand'] > 0, np.minimum(1.0, df['stock_level'] / df['daily_demand']), 1.0)
        return df

    def load_full_dataset(self):
        """
        Aggregate all product, inventory, and category data from APIs and simulation
        """
        results = {}
        products = self.fetch_products()
        if products is not None:
            results['products'] = products
            inventory = self.simulate_inventory_activity(products)
            if inventory is not None:
                results['inventory'] = inventory

        categories = self.fetch_categories()
        if categories is not None:
            results['categories'] = categories

        return results
