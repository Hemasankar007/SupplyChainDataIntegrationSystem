# Supply Chain Data Integration System

A modular Python system for extracting, processing, analyzing, and visualizing supply chain and logistics data from Excel files and APIs.

## Features

- **Data Extraction:**  
  - Reads logistics data from Excel sheets (`Orders`, `Returns`, `People`)
  - Fetches product and category data from external APIs (Fake Store API)
  - Simulates inventory activity and demand

- **Data Quality & Validation:**  
  - Automated checks for missing values, required columns, and price validity

- **Data Processing:**  
  - Calculates supply chain metrics (lead time, return rate, fill rate, turnover, stockout risk, etc.)

- **Data Warehouse:**  
  - Ready for integration with BigQuery or other data warehouses

- **Interactive Dashboard:**  
  - Streamlit dashboard for visualizing orders, inventory, returns, and analytics
  - Downloadable reports

## Folder Structure

```
Supply-Chain-Data-Integration-System-main/
│
├── main.py
├── config.py
├── utils/
│   ├── __init__.py
│   └── logger.py
├── data_extraction/
│   ├── __init__.py
│   ├── excel_connector.py
│   └── api_connector.py
├── data_processing/
│   ├── __init__.py
│   └── supply_chain_metrics.py
├── data_warehouse/
│   ├── __init__.py
│   └── bigquery_connector.py
├── dashboard/
│   ├── __init__.py
│   └── streamlit_app.py
└── README.md
```

## Getting Started

1. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

2. **Configure settings:**  
   Edit `config.py` to set file paths, API URLs, and other parameters.

3. **Run the main pipeline:**
    ```sh
    python main.py
    ```

4. **Launch the dashboard:**
    ```sh
    streamlit run dashboard/streamlit_app.py
    ```

## Key Metrics

- **Lead Time:** Average time from order to delivery
- **Return Rate:** Percentage of orders returned
- **Fill Rate:** Proportion of demand met from available inventory
- **Inventory Turnover:** Frequency of inventory replacement
- **Stockout Risk:** Products at risk of running out
- **Sales Metrics:** Total and average sales
- **Other metrics:** Customizable as needed

## Customization

- Add new metrics in `data_processing/supply_chain_metrics.py`
- Integrate more data sources in `data_extraction/`
- Extend dashboard features in `dashboard/streamlit_app.py`

## License

MIT License

---

**For questions or contributions, open an issue or pull request!**