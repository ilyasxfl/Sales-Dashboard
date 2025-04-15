from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import os
import base64
import io

# Initialize app with assets folder
app = Dash(__name__, assets_folder='assets')

# Default data
default_df = pd.read_csv(os.path.join('data', 'sales.csv'))

# Layout
app.layout = html.Div([
    html.H1("Sales Dashboard", style={
        'textAlign': 'center', 'color': '#00ff85', 'fontSize': '36px',
        'marginBottom': '20px', 'fontFamily': 'Arial, sans-serif'
    }),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload CSV', style={
            'background': '#00ff85', 'color': '#1a1a2e', 'border': 'none',
            'padding': '12px 24px', 'cursor': 'pointer', 'borderRadius': '5px',
            'fontSize': '16px', 'fontWeight': 'bold'
        }),
        accept='.csv',
        style={'textAlign': 'center', 'marginBottom': '20px'}
    ),
    html.Div(id='error-message', style={
        'color': '#ff4d4d', 'textAlign': 'center', 'fontSize': '14px',
        'marginBottom': '15px'
    }),
    html.Div([
        html.Label("Region:", style={
            'color': '#ffffff', 'marginRight': '10px', 'fontSize': '16px'
        }),
        dcc.Dropdown(id='region-filter', style={
            'width': '200px', 'display': 'inline-block', 'backgroundColor': '#0f3460',
            'color': '#ffffff', 'borderRadius': '5px'
        }, className='custom-dropdown'),
        html.Label("Date:", style={
            'color': '#ffffff', 'marginLeft': '20px', 'marginRight': '10px',
            'fontSize': '16px'
        }),
        dcc.Dropdown(id='date-filter', style={
            'width': '200px', 'display': 'inline-block', 'backgroundColor': '#0f3460',
            'color': '#ffffff', 'borderRadius': '5px'
        }, className='custom-dropdown'),
        html.Label("Product:", style={
            'color': '#ffffff', 'marginLeft': '20px', 'marginRight': '10px',
            'fontSize': '16px'
        }),
        dcc.Dropdown(id='product-filter', style={
            'width': '200px', 'display': 'inline-block', 'backgroundColor': '#0f3460',
            'color': '#ffffff', 'borderRadius': '5px'
        }, className='custom-dropdown'),
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),
    html.Div([
        dcc.Graph(id='sales-bar-chart', style={'width': '33%', 'display': 'inline-block'}),
        dcc.Graph(id='sales-pie-chart', style={'width': '33%', 'display': 'inline-block'}),
        dcc.Graph(id='sales-line-chart', style={'width': '33%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),
    dcc.Store(id='data-store', data=default_df.to_dict('records'))
], style={
    'background': '#1a1a2e', 'padding': '20px', 'minHeight': '100vh',
    'fontFamily': 'Arial, sans-serif'
})


# Parse uploaded CSV
def parse_csv(contents, filename):
    if not contents:
        return None, "No file uploaded."
    if not filename.endswith('.csv'):
        return None, "Please upload a CSV file."

    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        # Validate columns
        required_cols = ['date', 'region', 'product', 'sales']
        if not all(col in df.columns for col in required_cols):
            return None, f"CSV must have columns: {', '.join(required_cols)}."

        return df, ""
    except Exception as e:
        return None, f"Error processing file: {str(e)}."


# Update dropdowns and store data
@app.callback(
    [Output('region-filter', 'options'),
     Output('region-filter', 'value'),
     Output('date-filter', 'options'),
     Output('date-filter', 'value'),
     Output('product-filter', 'options'),
     Output('product-filter', 'value'),
     Output('error-message', 'children'),
     Output('data-store', 'data')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_dropdowns(contents, filename):
    df = default_df
    error = ""

    if contents is not None:
        df, error = parse_csv(contents, filename)
        if df is None:
            df = default_df
            error = error or "Failed to load CSV, using default data."

    regions = [{'label': r, 'value': r} for r in sorted(df['region'].unique())]
    dates = [{'label': d, 'value': d} for d in sorted(df['date'].unique())]
    products = [{'label': p, 'value': p} for p in sorted(df['product'].unique())]

    region_value = regions[0]['value'] if regions else None
    date_value = dates[0]['value'] if dates else None
    product_value = products[0]['value'] if products else None

    return regions, region_value, dates, date_value, products, product_value, error, df.to_dict('records')


# Update charts
@app.callback(
    [Output('sales-bar-chart', 'figure'),
     Output('sales-pie-chart', 'figure'),
     Output('sales-line-chart', 'figure')],
    [Input('region-filter', 'value'),
     Input('date-filter', 'value'),
     Input('product-filter', 'value'),
     Input('data-store', 'data')]
)
def update_charts(region, date, product, stored_data):
    df = pd.DataFrame(stored_data)

    if region is None or date is None or product is None or df.empty:
        return (
            px.bar(title="No Data Available"),
            px.pie(title="No Data Available"),
            px.line(title="No Data Available")
        )

    # Bar and Pie charts (specific date)
    filtered_df = df[(df['region'] == region) & (df['date'] == date)]
    if filtered_df.empty:
        return (
            px.bar(title="No Data for Selection"),
            px.pie(title="No Data for Selection"),
            px.line(title="No Data for Selection")
        )

    bar_fig = px.bar(filtered_df, x='date', y='sales', color='product',
                     title=f'Sales in {region} on {date}',
                     labels={'sales': 'Sales ($)', 'date': 'Date'})
    bar_fig.update_layout(
        plot_bgcolor='#0f3460', paper_bgcolor='#0f3460',
        font_color='#e0e0e0', title_font_color='#00ff85',
        margin=dict(l=20, r=20, t=50, b=20)
    )

    pie_fig = px.pie(filtered_df, values='sales', names='product',
                     title=f'Sales Distribution in {region} on {date}',
                     color_discrete_sequence=px.colors.qualitative.Plotly)
    pie_fig.update_layout(
        plot_bgcolor='#0f3460', paper_bgcolor='#0f3460',
        font_color='#e0e0e0', title_font_color='#00ff85',
        margin=dict(l=20, r=20, t=50, b=20)
    )

    # Line chart (all dates for region and product)
    line_df = df[(df['region'] == region) & (df['product'] == product)]
    line_fig = px.line(line_df, x='date', y='sales',
                       title=f'Sales Trend for {product} in {region}',
                       labels={'sales': 'Sales ($)', 'date': 'Date'})
    line_fig.update_traces(line_color='#00ff85', line_width=2)
    line_fig.update_layout(
        plot_bgcolor='#0f3460', paper_bgcolor='#0f3460',
        font_color='#e0e0e0', title_font_color='#00ff85',
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return bar_fig, pie_fig, line_fig


if __name__ == '__main__':
    app.run(debug=True)