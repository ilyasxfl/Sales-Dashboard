# Sales Dashboard

An interactive dashboard built with Python, Dash, and Plotly to visualize sales data by region, date, and product. Upload your own CSV, filter data, and explore insights with bar, pie, and line charts.

## Features
- **CSV Upload**: Load custom sales data (`date,region,product,sales`).
- **Filters**: Select region (e.g., Berlin), date (e.g., 2025-01-01), product (e.g., Laptop).
- **Charts**:
  - Bar: Compare sales by product/date.
  - Pie: See sales distribution.
  - Line: Track trends over time.
- **UI**: Dark theme, white dropdown text for readability.

## Use Cases
- **Sales Tracking**: Monitor performance across products or regions.
- **Inventory Management**: Optimize stock based on demand.
- **Market Analysis**: Identify top regions or seasonal trends.
- **Product Launches**: Evaluate new product sales.

## Installation
1. Clone: `git clone https://github.com/ilyasxfl/Sales-Dashboard`
2. Setup: `python -m venv .venv`
3. Activate:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Run: `python main.py`
6. Open: `http://127.0.0.1:8050`

## Files
- `main.py`: Dashboard app.
- `data\sales.csv`: Sample data.
- `assets\style.css`: Custom styling.
- `requirements.txt`: Dependencies.

## Screenshot
[Coming soon]

## License
MIT
