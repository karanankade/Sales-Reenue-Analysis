"""
Sales & Revenue Analysis Dashboard
Built with Plotly Dash
"""
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from data_processor import (
    load_and_process_data,
    get_kpi_metrics,
    get_revenue_trend,
    get_top_products,
    get_sales_by_segment,
    get_sales_by_country,
    get_unique_values
)
import os

# Load data
data_file = os.path.join(os.path.dirname(__file__), 'Financial Sample.xlsx')
df = load_and_process_data(data_file)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Sales & Revenue Analysis Dashboard"

# Get unique values for filters
filter_values = get_unique_values(df)

# Define the layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("📊 Sales & Revenue Analysis Dashboard", style={'color': 'white', 'marginBottom': 10}),
        html.P("Interactive business intelligence dashboard with KPI tracking and revenue analysis", 
               style={'color': '#e0e0e0', 'marginTop': 0})
    ], style={
        'backgroundColor': '#1f77b4',
        'padding': '20px',
        'marginBottom': '20px',
        'borderRadius': '5px'
    }),
    
    # Filters Section
    html.Div([
        html.H3("🔍 Filters", style={'marginBottom': 15}),
        html.Div([
            # Year Filter
            html.Div([
                html.Label("Year:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='year-filter',
                    options=[{'label': 'All Years', 'value': 'all'}] + 
                            [{'label': str(year), 'value': year} for year in filter_values['years']],
                    value='all',
                    clearable=False
                )
            ], style={'flex': 1, 'marginRight': '10px'}),
            
            # Segment Filter
            html.Div([
                html.Label("Segment:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='segment-filter',
                    options=[{'label': 'All Segments', 'value': 'all'}] + 
                            [{'label': seg, 'value': seg} for seg in filter_values['segments']],
                    value='all',
                    clearable=False
                )
            ], style={'flex': 1, 'marginRight': '10px'}),
            
            # Country Filter
            html.Div([
                html.Label("Country:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='country-filter',
                    options=[{'label': 'All Countries', 'value': 'all'}] + 
                            [{'label': country, 'value': country} for country in filter_values['countries']],
                    value='all',
                    clearable=False
                )
            ], style={'flex': 1, 'marginRight': '10px'}),
            
            # Product Filter
            html.Div([
                html.Label("Product:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='product-filter',
                    options=[{'label': 'All Products', 'value': 'all'}] + 
                            [{'label': prod, 'value': prod} for prod in filter_values['products']],
                    value='all',
                    clearable=False
                )
            ], style={'flex': 1})
        ], style={'display': 'flex', 'gap': '10px'})
    ], style={
        'backgroundColor': '#f8f9fa',
        'padding': '15px',
        'marginBottom': '20px',
        'borderRadius': '5px',
        'border': '1px solid #dee2e6'
    }),
    
    # KPI Cards
    html.Div(id='kpi-cards', style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
        'gap': '15px',
        'marginBottom': '20px'
    }),
    
    # Main Charts
    html.Div([
        # Revenue Trend
        html.Div([
            dcc.Graph(id='revenue-trend-chart')
        ], style={'marginBottom': '20px'}),
        
        # Top Products vs Sales by Segment
        html.Div([
            html.Div([
                dcc.Graph(id='top-products-chart')
            ], style={'flex': 1, 'marginRight': '10px'}),
            html.Div([
                dcc.Graph(id='segment-chart')
            ], style={'flex': 1})
        ], style={'display': 'flex', 'marginBottom': '20px'}),
        
        # Sales by Country
        html.Div([
            dcc.Graph(id='country-chart')
        ], style={'marginBottom': '20px'}),
        
        # Profit vs Sales Scatter
        html.Div([
            dcc.Graph(id='scatter-chart')
        ])
    ])
    
], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#ffffff'})


# Callback for filtering data
@callback(
    Output('kpi-cards', 'children'),
    Output('revenue-trend-chart', 'figure'),
    Output('top-products-chart', 'figure'),
    Output('segment-chart', 'figure'),
    Output('country-chart', 'figure'),
    Output('scatter-chart', 'figure'),
    Input('year-filter', 'value'),
    Input('segment-filter', 'value'),
    Input('country-filter', 'value'),
    Input('product-filter', 'value')
)
def update_dashboard(selected_year, selected_segment, selected_country, selected_product):
    # Filter data
    filtered_df = df.copy()
    
    if selected_year != 'all':
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    
    if selected_segment != 'all':
        filtered_df = filtered_df[filtered_df['Segment'] == selected_segment]
    
    if selected_country != 'all':
        filtered_df = filtered_df[filtered_df['Country'] == selected_country]
    
    if selected_product != 'all':
        filtered_df = filtered_df[filtered_df['Product'] == selected_product]
    
    # Calculate KPIs
    kpis = get_kpi_metrics(filtered_df)
    
    # Create KPI Cards
    kpi_cards = [
        html.Div([
            html.H4("Total Sales", style={'color': '#666', 'marginBottom': 10}),
            html.H2(f"${kpis['total_sales']:,.0f}", style={'color': '#1f77b4', 'margin': 0})
        ], style={
            'backgroundColor': '#f0f8ff',
            'padding': '20px',
            'borderRadius': '5px',
            'border': '2px solid #1f77b4',
            'textAlign': 'center'
        }),
        
        html.Div([
            html.H4("Total Profit", style={'color': '#666', 'marginBottom': 10}),
            html.H2(f"${kpis['total_profit']:,.0f}", style={'color': '#2ca02c', 'margin': 0})
        ], style={
            'backgroundColor': '#f0fff0',
            'padding': '20px',
            'borderRadius': '5px',
            'border': '2px solid #2ca02c',
            'textAlign': 'center'
        }),
        
        html.Div([
            html.H4("Total Units Sold", style={'color': '#666', 'marginBottom': 10}),
            html.H2(f"{kpis['total_units']:,.0f}", style={'color': '#ff7f0e', 'margin': 0})
        ], style={
            'backgroundColor': '#fffaf0',
            'padding': '20px',
            'borderRadius': '5px',
            'border': '2px solid #ff7f0e',
            'textAlign': 'center'
        }),
        
        html.Div([
            html.H4("Profit Margin", style={'color': '#666', 'marginBottom': 10}),
            html.H2(f"{kpis['avg_profit_margin']:.1f}%", style={'color': '#d62728', 'margin': 0})
        ], style={
            'backgroundColor': '#fff0f0',
            'padding': '20px',
            'borderRadius': '5px',
            'border': '2px solid #d62728',
            'textAlign': 'center'
        })
    ]
    
    # Revenue Trend Chart
    revenue_trend = get_revenue_trend(filtered_df)
    revenue_fig = go.Figure()
    revenue_fig.add_trace(go.Scatter(
        x=revenue_trend['Date'],
        y=revenue_trend['Sales'],
        name='Sales',
        mode='lines+markers',
        line=dict(color='#1f77b4', width=2),
        fill='tozeroy'
    ))
    revenue_fig.add_trace(go.Scatter(
        x=revenue_trend['Date'],
        y=revenue_trend['Profit'],
        name='Profit',
        mode='lines+markers',
        line=dict(color='#2ca02c', width=2),
        yaxis='y2'
    ))
    revenue_fig.update_layout(
        title='Revenue & Profit Trend Over Time',
        xaxis_title='Date',
        yaxis_title='Sales ($)',
        yaxis2=dict(
            title='Profit ($)',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    # Top Products Chart
    top_products = get_top_products(filtered_df, top_n=10)
    top_prod_fig = px.bar(
        top_products,
        x='Sales',
        y='Product',
        orientation='h',
        title='Top 10 Products by Sales',
        labels={'Sales': 'Sales ($)', 'Product': 'Product'},
        color='Sales',
        color_continuous_scale='Blues',
        template='plotly_white'
    )
    top_prod_fig.update_layout(height=400, showlegend=False)
    
    # Segment Chart
    segment_data = get_sales_by_segment(filtered_df)
    segment_fig = px.pie(
        segment_data,
        values='Sales',
        names='Segment',
        title='Sales Distribution by Segment',
        template='plotly_white'
    )
    segment_fig.update_layout(height=400)
    
    # Country Chart
    country_data = get_sales_by_country(filtered_df).head(10)
    country_fig = px.bar(
        country_data,
        x='Country',
        y='Sales',
        title='Top 10 Countries by Sales',
        labels={'Sales': 'Sales ($)', 'Country': 'Country'},
        color='Profit',
        color_continuous_scale='Viridis',
        template='plotly_white'
    )
    country_fig.update_layout(
        height=400,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    # Scatter Chart - Profit vs Sales by Product
    scatter_data = filtered_df.groupby('Product').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Units Sold': 'sum'
    }).reset_index()
    
    scatter_fig = px.scatter(
        scatter_data,
        x='Sales',
        y='Profit',
        size='Units Sold',
        color='Units Sold',
        hover_name='Product',
        title='Profit vs Sales by Product (bubble size = units sold)',
        labels={'Sales': 'Total Sales ($)', 'Profit': 'Total Profit ($)'},
        color_continuous_scale='Reds',
        template='plotly_white'
    )
    scatter_fig.update_layout(height=400)
    
    return kpi_cards, revenue_fig, top_prod_fig, segment_fig, country_fig, scatter_fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
