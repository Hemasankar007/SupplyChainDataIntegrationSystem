# Supply Chain Data Integration System

This is a modular Python system designed for extracting, processing, analyzing, and visualizing supply chain and logistics data. It integrates data from various sources like Excel files and APIs, performs data quality checks, calculates key supply chain metrics, and provides an interactive dashboard for visualization.

## Features

*   **Data Extraction:** Ingests logistics data from Excel sheets (Orders, Returns, People) and fetches product/category data from external APIs.
*   **Data Quality & Validation:** Automated checks for data integrity, missing values, and validity.
*   **Data Processing:** Calculates essential supply chain metrics such as lead time, return rate, fill rate, inventory turnover, and stockout risk.
*   **Data Warehouse Integration:** Designed for easy integration with data warehouses like Google BigQuery.
*   **Interactive Dashboard:** A Streamlit-based dashboard for visualizing orders, inventory, returns, and analytics, with options for downloadable reports.

## Getting Started

Follow these steps to set up and run the project:

### 1. Install Dependencies

First, install all the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 2. Configure Settings (Optional)

Review and modify the `settings.py` file to adjust file paths, API URLs, or other parameters as needed for your environment.

### 3. Run the Main Data Pipeline

Execute the `main.py` script to run the data ingestion, transformation, and loading processes. This will prepare the data for the dashboard.

```bash
python main.py
```

### 4. Launch the Streamlit Dashboard

After the data pipeline has run, you can launch the interactive dashboard using Streamlit. Navigate to the project's root directory in your terminal and run:

```bash
streamlit run dashboard.py
```

This command will open the Streamlit application in your web browser, typically at `http://localhost:8501`.

## Project Structure

```
Supply-Chain-Data-Integration-System-main/
├── main.py                 # Main script to run the data pipeline
├── dashboard.py            # Streamlit application for the dashboard
├── requirements.txt        # Python dependencies
├── settings.py             # Configuration settings
├── PROJECT_OVERVIEW.md     # Detailed project overview
├── helpers/                # Utility functions (e.g., logging)
│   └── logging_utils.py
├── ingestion/              # Data ingestion modules
│   ├── api_ingestor.py
│   └── excel_ingestor.py
├── logs/                   # Log files
├── transformation/         # Data transformation and metric calculation
│   └── metrics_calculator.py
└── warehouse/              # Data warehouse integration
    └── bigquery_manager.py
```

## Key Metrics Calculated

*   **Lead Time:** Time from order placement to delivery.
*   **Return Rate:** Percentage of orders returned.
*   **Fill Rate:** Proportion of demand met from available inventory.
*   **Inventory Turnover:** How many times inventory is sold and replaced over a period.
*   **Stockout Risk:** Probability of running out of stock for a product.
*   **Sales Metrics:** Total and average sales.

## Customization

*   **New Metrics:** Add custom metrics in `transformation/metrics_calculator.py`.
*   **Data Sources:** Integrate additional data sources by extending modules in `ingestion/`.
*   **Dashboard Features:** Enhance the dashboard's functionality and visualizations in `dashboard.py`.

