import pandas as pd
import os
import kaggle
from datetime import datetime
from helpers.logging_utils import record_pipeline_event, record_data_validation
from settings import DATA_DIR, EXCEL_FILE_PATH, KAGGLE_DATASET_NAME

class ExcelDataIntegrator:
    """
    Manages extraction, validation, and transformation of Excel-based logistics data
    """

    def __init__(self):
        self.logger = record_pipeline_event("ExcelDataIntegrator", "INITIALIZED")
        self.data_dir = DATA_DIR
        self.excel_path = EXCEL_FILE_PATH

    def fetch_dataset_from_kaggle(self):
        """
        Download dataset from Kaggle and extract
        """
        try:
            self.logger.info("Starting dataset download from Kaggle...")
            os.makedirs(self.data_dir, exist_ok=True)
            kaggle.api.dataset_download_files(
                KAGGLE_DATASET_NAME,
                path=self.data_dir,
                unzip=True
            )
            self.logger.info("Dataset downloaded and extracted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Dataset download failed: {str(e)}")
            return False

    def read_orders_sheet(self):
        try:
            self.logger.info("Reading Orders sheet...")
            df = pd.read_excel(self.excel_path, sheet_name='Orders')
            self._check_orders_quality(df)
            df = self._process_orders_data(df)
            self.logger.info(f"Orders data loaded. Rows: {df.shape[0]}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to read Orders: {str(e)}")
            return None

    def read_returns_sheet(self):
        try:
            self.logger.info("Reading Returns sheet...")
            df = pd.read_excel(self.excel_path, sheet_name='Returns')
            self._check_returns_quality(df)
            df = self._process_returns_data(df)
            self.logger.info(f"Returns data loaded. Rows: {df.shape[0]}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to read Returns: {str(e)}")
            return None

    def read_people_sheet(self):
        try:
            self.logger.info("Reading People sheet...")
            df = pd.read_excel(self.excel_path, sheet_name='People')
            self._check_people_quality(df)
            df = self._process_people_data(df)
            self.logger.info(f"People data loaded. Rows: {df.shape[0]}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to read People: {str(e)}")
            return None

    def _check_orders_quality(self, df):
        missing = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        status = "PASS" if missing <= 0.05 else "WARNING"
        record_data_validation("Orders Missing Data", status, f"{missing:.2%} missing")

        required = ['Order ID', 'Order Date', 'Ship Date', 'Customer ID', 'Product ID']
        missing_cols = [c for c in required if c not in df.columns]
        status = "PASS" if not missing_cols else "FAIL"
        record_data_validation("Orders Required Columns", status, str(missing_cols) if missing_cols else "All present")

    def _check_returns_quality(self, df):
        missing = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        status = "PASS" if missing <= 0.05 else "WARNING"
        record_data_validation("Returns Missing Data", status, f"{missing:.2%} missing")

    def _check_people_quality(self, df):
        missing = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        status = "PASS" if missing <= 0.05 else "WARNING"
        record_data_validation("People Missing Data", status, f"{missing:.2%} missing")

    def _process_orders_data(self, df):
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'])
            df['Order Year'] = df['Order Date'].dt.year
            df['Order Month'] = df['Order Date'].dt.month
            df['Order Quarter'] = df['Order Date'].dt.quarter

        if 'Ship Date' in df.columns:
            df['Ship Date'] = pd.to_datetime(df['Ship Date'])

        if 'Order Date' in df.columns and 'Ship Date' in df.columns:
            df['Lead Time (Days)'] = (df['Ship Date'] - df['Order Date']).dt.days

        if 'Sales' in df.columns and 'Quantity' in df.columns:
            df['Order Value'] = df['Sales'] * df['Quantity']

        return df

    def _process_returns_data(self, df):
        if 'Return Date' in df.columns:
            df['Return Date'] = pd.to_datetime(df['Return Date'])
        return df

    def _process_people_data(self, df):
        if 'Person' not in df.columns:
            df['Person'] = 'Unknown'
        return df

    def load_complete_dataset(self):
        dataset = {
            'orders': self.read_orders_sheet(),
            'returns': self.read_returns_sheet(),
            'people': self.read_people_sheet()
        }
        return dataset