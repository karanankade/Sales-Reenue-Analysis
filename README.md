# 📊 Sales & Revenue Analysis Dashboard

A comprehensive interactive business intelligence dashboard built with Plotly Dash for analyzing sales and revenue data.

## Features

### 🎯 Key Performance Indicators (KPIs)
- **Total Sales**: Sum of all sales transactions
- **Total Profit**: Net profit across all products and regions
- **Total Units Sold**: Complete unit volume across transactions
- **Profit Margin**: Average profit margin percentage

### 📈 Visualizations

1. **Revenue & Profit Trend** - Line chart showing sales and profit trends over time with dual axes
2. **Top 10 Products by Sales** - Horizontal bar chart highlighting best-performing products
3. **Sales by Segment** - Pie chart showing market segment distribution
4. **Top 10 Countries by Sales** - Bar chart with profit metrics overlay
5. **Profit vs Sales Scatter Plot** - Bubble chart showing product performance (bubble size = units sold)

### 🔍 Interactive Filters
- **Year Filter**: Select specific years or view all data
- **Segment Filter**: Filter by market segment (Government, Midmarket, Enterprise, etc.)
- **Country Filter**: Drill down by specific countries
- **Product Filter**: Analyze individual products

All charts update dynamically based on filter selections.

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the dashboard:**
```bash
python app.py
```

3. **Access the dashboard:**
Open your browser and navigate to `http://localhost:8050`

## Project Structure

```
.
├── app.py                      # Main Dash application
├── data_processor.py           # Data loading and processing functions
├── requirements.txt            # Python dependencies
├── Financial Sample.xlsx       # Sample sales data
└── README.md                   # This file
```

## Data Source

The dashboard uses **Financial Sample.xlsx** containing 700 transaction records with:
- **Segments**: Government, Midmarket, Enterprise
- **Countries**: Multiple international markets
- **Products**: Various product lines
- **Time Period**: 2014-2018 data
- **Metrics**: Sales, Profit, Units, Manufacturing Cost, etc.

## Key Insights You Can Discover

✅ **Seasonal Trends** - Identify peak sales periods and seasonal patterns  
✅ **Product Performance** - Find top-selling and high-margin products  
✅ **Geographic Analysis** - Compare sales performance across countries  
✅ **Segment Performance** - Analyze profit margins by customer segment  
✅ **Growth Opportunities** - Spot underperforming products and markets  

## Technologies Used

- **Dash** (v2.14.2) - Interactive web application framework
- **Plotly** (v5.17.0) - Advanced data visualization
- **Pandas** (v2.1.1) - Data manipulation and analysis
- **Python** (3.8+) - Programming language

## How to Extend

### Add New Visualizations
Edit `app.py` and add new `dcc.Graph()` components in the layout, then create corresponding callback outputs.

### Add New Filters
Add dropdown elements in the filter section and include them in the callback conditions.

### Use Different Data Source
Update `data_processor.py` to load data from:
- CSV files
- SQL databases
- REST APIs
- Other Excel files

### Modify KPI Calculations
Edit `get_kpi_metrics()` in `data_processor.py` to calculate custom metrics.

## Learning Outcomes

By working with this dashboard, you'll learn:
- 📊 **Data Visualization** - Creating interactive charts with Plotly
- 📉 **KPI Tracking** - Defining and calculating key performance indicators
- 🔄 **Interactive Filtering** - Building responsive dashboards with callbacks
- 💼 **Business Intelligence** - Extracting insights from sales data
- 🐍 **Python Data Analysis** - Using Pandas for data manipulation
- 🎨 **UI/UX Design** - Creating intuitive dashboards

## Troubleshooting

**Port 8050 already in use:**
```bash
python app.py --port 8051
```

**Missing dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

**Excel file not found:**
Ensure `Financial Sample.xlsx` is in the same directory as `app.py`

## Future Enhancements

- 📥 Add data upload functionality for custom datasets
- 📊 Export reports to PDF/Excel
- 🔐 Add user authentication
- 📱 Mobile-responsive design improvements
- 🤖 Predictive analytics and forecasting
- 🔔 Alerts for anomalies and thresholds
- 💾 Database integration for real-time data

---

**Happy analyzing! 🚀**
