from dash import Dash, dcc, html
import dash_leaflet as dl
from .data.data import load_data
from .callbacks.map import register_map_callbacks
from .callbacks.charts import register_chart_callbacks

# Load data
issues_values_joined, property_values, issues = load_data()

# Initialize the app
app = Dash(__name__)
server = app.server

# Layout
app.layout = html.Div([
    html.Div([
        dl.Map(
            id='city-map',
            style={'width': '100%', 'height': '400px'},
            center=[49.272877, -123.078896],
            zoom=11.2,
        ),
        dcc.Dropdown(
            id='region-dropdown',
            options=[
                {'label': loc, 'value': loc} for loc in sorted(property_values['geo_local_area'].unique())
            ],
            value=None,
            placeholder='Select a Neighbourhood'
        ),
        dcc.Dropdown(
            id='zoning-dropdown',
            options=[
                {'label': loc, 'value': loc} for loc in sorted(property_values['zoning_classification'].unique())
            ],
            value=None,
            placeholder='Select a Zoning Type'
        )
    ], style={'width': '50%', 'display': 'inline-block'}),
    
    html.Div([
        html.Iframe(
            id='pie-chart',
            style={'width': '100%', 'height': '400px', 'border': 'none'}
        ),
        html.Iframe(
            id='bar-chart',
            style={'width': '100%', 'height': '300px', 'border': 'none'}
        ),
        html.Iframe(
            id='scatter-plot',
            style={'width': '100%', 'height': '400px', 'border': 'none'}
        )
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
])

# Register callbacks
register_map_callbacks(app, issues_values_joined)
register_chart_callbacks(app, issues, issues_values_joined, property_values)

# Run the app
if __name__ == '__main__':
    app.server.run(host='127.0.0.1', port=8050)
