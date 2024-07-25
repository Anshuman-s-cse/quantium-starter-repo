import pytest
from dash import dcc, html
import dash
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import dash_daq as daq

# Sample data for testing
data = {
    'product': ['pink morsel', 'pink morsel', 'pink morsel', 'pink morsel', 'gold morsel'],
    'price': ['$3.00', '$3.00', '$3.00', '$3.00', '$9.99'],
    'quantity': [526, 546, 505, 561, 553],
    'date': ['2020-10-13', '2020-10-13', '2020-10-13', '2020-10-13', '2020-10-13'],
    'region': ['north', 'south', 'east', 'west', 'north']
}
df = pd.DataFrame(data)
df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
df['sales'] = df['price'] * df['quantity']
df['date'] = pd.to_datetime(df['date'])

# Define the app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Pink Morsel Sales Data'),
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
    dcc.Graph(id='sales-graph')
])

@app.callback(
    Output('sales-graph', 'figure'),
    [Input('region-radio', 'value')]
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_data = df
    else:
        filtered_data = df[df['region'] == selected_region]
    fig = px.line(filtered_data, x='date', y='sales', color='region', title='Sales Over Time')
    return fig

# Tests
def test_app_loading(dash_duo):
    dash_duo.start_server(app)
    assert dash_duo.find_element('#region-radio') is not None
    assert dash_duo.find_element('#sales-graph') is not None

def test_radio_buttons(dash_duo):
    dash_duo.start_server(app)
    radio_button = dash_duo.find_element('#region-radio')
    options = radio_button.find_elements_by_tag_name('input')
    assert len(options) == 5  # Check there are 5 options

def test_graph_update(dash_duo):
    dash_duo.start_server(app)
    dash_duo.find_element('#region-radio').find_element_by_xpath("//input[@value='north']").click()
    assert 'Sales Over Time' in dash_duo.find_element('#sales-graph').get_attribute('innerHTML')

if __name__ == '__main__':
    pytest.main()

