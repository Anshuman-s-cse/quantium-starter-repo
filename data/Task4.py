import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Load data
file_path = 'daily_sales_data.csv'
sales_data = pd.read_csv(file_path)

# Create Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1(children='Pink Morsel Sales Data'),

    dcc.RadioItems(
        id='region-radio',
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': 'North', 'value': 'north'},
            {'label': 'East', 'value': 'east'},
            {'label': 'South', 'value': 'south'},
            {'label': 'West', 'value': 'west'}
        ],
        value='all'
    ),

    dcc.Graph(
        id='sales-graph'
    )
])

# Callback to update graph based on selected region
@app.callback(
    Output('sales-graph', 'figure'),
    [Input('region-radio', 'value')]
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_data = sales_data
    else:
        filtered_data = sales_data[sales_data['region'] == selected_region]

    fig = px.line(filtered_data, x='date', y='sales', color='region', title='Sales Over Time')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
