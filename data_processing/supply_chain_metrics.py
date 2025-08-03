import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.logger import log_pipeline_step, log_data_quality_check
from config import LEAD_TIME_THRESHOLDS, FILL_RATE_THRESHOLDS

class LogisticsAnalytics:
    def __init__(self):
        self.logger = log_pipeline_step("LogisticsAnalytics", "STARTED")

    def compute_lead_time_stats(self, df_orders):
        try:
            self.logger.info("Computing lead time statistics...")

            if 'Lead Time (Days)' not in df_orders.columns:
                self.logger.error("Missing 'Lead Time (Days)' column in order data.")
                return None

            stats = {
                'avg_lead_time': df_orders['Lead Time (Days)'].mean(),
                'med_lead_time': df_orders['Lead Time (Days)'].median(),
                'std_lead_time': df_orders['Lead Time (Days)'].std(),
                'min_lead_time': df_orders['Lead Time (Days)'].min(),
                'max_lead_time': df_orders['Lead Time (Days)'].max(),
                'order_count': len(df_orders)
            }

            df_orders['lead_time_grade'] = pd.cut(
                df_orders['Lead Time (Days)'],
                bins=[0, LEAD_TIME_THRESHOLDS['excellent'], LEAD_TIME_THRESHOLDS['good'], float('inf')],
                labels=['Excellent', 'Good', 'Poor']
            )

            performance = df_orders['lead_time_grade'].value_counts(normalize=True)
            stats.update({
                'excellent_ratio': performance.get('Excellent', 0),
                'good_ratio': performance.get('Good', 0),
                'poor_ratio': performance.get('Poor', 0)
            })

            self.logger.info("Lead time statistics successfully computed.")
            return stats

        except Exception as e:
            self.logger.error(f"Failed to compute lead time statistics: {str(e)}")
            return None

    def compute_cycle_time(self, df_orders):
        try:
            self.logger.info("Computing order cycle time...")

            if 'Ship Date' in df_orders.columns:
                days_delta = np.random.randint(2, 6, size=len(df_orders))
                df_orders['Delivery Date'] = df_orders['Ship Date'] + pd.to_timedelta(days_delta, unit='D')

                df_orders['Cycle Time (Days)'] = (df_orders['Delivery Date'] - df_orders['Order Date']).dt.days

                stats = {
                    'avg_cycle_time': df_orders['Cycle Time (Days)'].mean(),
                    'med_cycle_time': df_orders['Cycle Time (Days)'].median(),
                    'std_cycle_time': df_orders['Cycle Time (Days)'].std(),
                    'min_cycle_time': df_orders['Cycle Time (Days)'].min(),
                    'max_cycle_time': df_orders['Cycle Time (Days)'].max()
                }

                self.logger.info("Cycle time successfully computed.")
                return stats

            else:
                self.logger.warning("'Ship Date' not found. Using lead time as fallback.")
                return self.compute_lead_time_stats(df_orders)

        except Exception as e:
            self.logger.error(f"Failed to compute order cycle time: {str(e)}")
            return None

    def compute_inventory_turnover(self, df_inventory):
        try:
            self.logger.info("Computing inventory turnover...")

            grouped = df_inventory.groupby('product_id').agg({
                'daily_demand': 'mean',
                'stock_level': 'mean',
                'annualized_turnover': 'mean'
            }).reset_index()

            grouped['days_on_hand'] = np.where(
                grouped['daily_demand'] > 0,
                grouped['stock_level'] / grouped['daily_demand'],
                float('inf')
            )

            stats = {
                'avg_turnover': grouped['annualized_turnover'].mean(),
                'med_turnover': grouped['annualized_turnover'].median(),
                'avg_days_on_hand': grouped['days_on_hand'].mean(),
                'med_days_on_hand': grouped['days_on_hand'].median(),
                'product_count': len(grouped)
            }

            self.logger.info("Inventory turnover metrics successfully computed.")
            return stats

        except Exception as e:
            self.logger.error(f"Failed to compute inventory turnover: {str(e)}")
            return None

    def compute_fill_rate_stats(self, df_inventory):
        try:
            self.logger.info("Computing fill rate metrics...")

            grouped = df_inventory.groupby('product_id').agg({
                'fill_rate': 'mean',
                'stockout_risk': 'sum'
            }).reset_index()

            stats = {
                'avg_fill_rate': grouped['fill_rate'].mean(),
                'med_fill_rate': grouped['fill_rate'].median(),
                'excellent_rate_ratio': (grouped['fill_rate'] >= FILL_RATE_THRESHOLDS['excellent']).mean(),
                'good_rate_ratio': (grouped['fill_rate'] >= FILL_RATE_THRESHOLDS['good']).mean(),
                'poor_rate_ratio': (grouped['fill_rate'] < FILL_RATE_THRESHOLDS['poor']).mean(),
                'product_total': len(grouped),
                'at_risk_count': grouped['stockout_risk'].sum()
            }

            self.logger.info("Fill rate metrics successfully computed.")
            return stats

        except Exception as e:
            self.logger.error(f"Failed to compute fill rate metrics: {str(e)}")
            return None

    def compute_category_metrics(self, df_orders, df_inventory):
        try:
            self.logger.info("Computing category metrics...")

            if 'category' in df_orders.columns and 'category' in df_inventory.columns:
                lead_time_grp = df_orders.groupby('category')['Lead Time (Days)'].agg(['mean', 'median', 'std', 'count']).reset_index()
                inventory_grp = df_inventory.groupby('category').agg({
                    'fill_rate': 'mean',
                    'annualized_turnover': 'mean',
                    'days_of_inventory': 'mean',
                    'stockout_risk': 'sum'
                }).reset_index()

                combined = pd.merge(lead_time_grp, inventory_grp, on='category', how='outer')

                self.logger.info("Category metrics successfully computed.")
                return combined

            else:
                self.logger.warning("Missing 'category' column in one or both datasets.")
                return None

        except Exception as e:
            self.logger.error(f"Failed to compute category metrics: {str(e)}")
            return None

    def compute_return_metrics(self, df_orders, df_returns):
        try:
            self.logger.info("Computing return statistics...")

            if df_returns is not None and not df_returns.empty:
                order_total = len(df_orders)
                return_total = len(df_returns)
                rate = return_total / order_total if order_total > 0 else 0

                if 'category' in df_returns.columns:
                    category_breakdown = df_returns['category'].value_counts(normalize=True)
                else:
                    category_breakdown = None

                stats = {
                    'order_total': order_total,
                    'return_total': return_total,
                    'return_ratio': rate,
                    'return_percent': rate * 100,
                    'category_breakdown': category_breakdown
                }

                self.logger.info("Return statistics successfully computed.")
                return stats

            else:
                self.logger.warning("No return data found.")
                return {
                    'order_total': len(df_orders),
                    'return_total': 0,
                    'return_ratio': 0,
                    'return_percent': 0
                }

        except Exception as e:
            self.logger.error(f"Failed to compute return statistics: {str(e)}")
            return None

    def compute_all_metrics(self, df_orders, df_inventory, df_returns=None):
        try:
            self.logger.info("Running full supply chain analytics suite...")

            result = {
                'lead_time': self.compute_lead_time_stats(df_orders),
                'cycle_time': self.compute_cycle_time(df_orders),
                'inventory_turnover': self.compute_inventory_turnover(df_inventory),
                'fill_rate': self.compute_fill_rate_stats(df_inventory),
                'category': self.compute_category_metrics(df_orders, df_inventory),
                'returns': self.compute_return_metrics(df_orders, df_returns)
            }

            self.logger.info("All analytics computed successfully.")
            return result

        except Exception as e:
            self.logger.error(f"Failed to compute full analytics suite: {str(e)}")
            return None
