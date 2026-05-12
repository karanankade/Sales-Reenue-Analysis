"""
Data processing module for Sales & Revenue Dashboard
"""
import pandas as pd
import os


def load_and_process_data(filepath):
    """
    Load and process the Financial Sample data

    Parameters:
    -----------
    filepath : str
        Path to the Excel file

    Returns:
    --------
    pd.DataFrame
        Processed dataframe with cleaned column names
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Data file not found: {filepath}. "
            "Make sure 'Financial Sample.xlsx' is committed to the repository."
        )

    try:
        df = pd.read_excel(filepath, engine='openpyxl')
    except Exception as e:
        raise RuntimeError(f"Failed to read Excel file '{filepath}': {e}")

    # Clean column names — strip ALL whitespace (leading, trailing, internal)
    df.columns = [str(col).strip() for col in df.columns]

    # Rename any columns with internal spaces variations to canonical names
    col_map = {}
    for col in df.columns:
        normalized = ' '.join(col.split())  # collapse multiple spaces
        if normalized != col:
            col_map[col] = normalized
    if col_map:
        df.rename(columns=col_map, inplace=True)

    # Ensure required columns exist
    required_columns = ['Date', 'Sales', 'Profit', 'Units Sold', 'Year',
                        'Product', 'Segment', 'Country']
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}. "
            f"Available columns: {list(df.columns)}"
        )

    # Convert Date to datetime if not already
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows with unparseable dates
    df = df.dropna(subset=['Date'])

    # Ensure Year column is integer
    df['Year'] = df['Year'].astype(int)

    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)

    return df


def get_kpi_metrics(df):
    """
    Calculate key performance indicators
    
    Returns:
    --------
    dict
        Dictionary containing KPI metrics
    """
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_units = df['Units Sold'].sum()
    avg_profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    
    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'total_units': total_units,
        'avg_profit_margin': avg_profit_margin
    }


def get_revenue_trend(df):
    """Get monthly revenue trend"""
    monthly_data = df.groupby([df['Date'].dt.to_period('M')]).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index()
    
    monthly_data['Date'] = monthly_data['Date'].dt.to_timestamp()
    return monthly_data.sort_values('Date')


def get_top_products(df, top_n=10):
    """Get top performing products by sales"""
    return df.groupby('Product').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Units Sold': 'sum'
    }).sort_values('Sales', ascending=False).head(top_n).reset_index()


def get_sales_by_segment(df):
    """Get sales breakdown by segment"""
    return df.groupby('Segment').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index().sort_values('Sales', ascending=False)


def get_sales_by_country(df):
    """Get sales breakdown by country"""
    return df.groupby('Country').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index().sort_values('Sales', ascending=False)


def get_unique_values(df):
    """Get unique values for filters"""
    return {
        'products': sorted(df['Product'].unique().tolist()),
        'segments': sorted(df['Segment'].unique().tolist()),
        'countries': sorted(df['Country'].unique().tolist()),
        'years': sorted(df['Year'].unique().tolist())
    }
