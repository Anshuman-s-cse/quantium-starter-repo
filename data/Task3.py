from dash import Dash, dcc, html
import pandas as pd
import plotly.graph_objs as go

# Correct file path
file_path = 'daily_sales_data.csv'

# Load the formatted data
try:
    sales_data = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
    exit(1)

# Convert 'date' column to datetime
sales_data['date'] = pd.to_datetime(sales_data['date'])

# Aggregate sales by date
daily_sales = sales_data.groupby('date').sum().reset_index()

# Create the Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Soul Foods Sales Visualiser'),

    dcc.Graph(
        id='sales-line-chart',
        figure={
            'data': [
                go.Scatter(
                    x=daily_sales['date'],
                    y=daily_sales['sales'],
                    mode='lines',
                    name='Sales'
                )
            ],
            'layout': go.Layout(
                title='Daily Sales of Pink Morsels',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Sales'},
                shapes=[
                    {
                        'type': 'line',
                        'x0': '2021-01-15',
                        'x1': '2021-01-15',
                        'y0': 0,
                        'y1': max(daily_sales['sales']),
                        'line': {
                            'color': 'red',
                            'width': 2,
                            'dash': 'dash',
                        },
                        'name': 'Price Increase'
                    }
                ]
            )
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
