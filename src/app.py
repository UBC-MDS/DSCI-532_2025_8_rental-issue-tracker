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
    # Title Section
    html.Div([
        html.H1("Vancouver Rental Issue Tracker Dashboard", 
                style={'textAlign': 'center', 'marginBottom': '20px'})
    ], style={'width': '100%', 'padding': '10px', 'backgroundColor': '#f9f9f9', 
              'margin': '0 auto'}),

    # Main Content Section (Grid Layout)
    html.Div([
        # Row 1: Map and Dropdowns (Left Column)
        html.Div([
            html.Div([
                dl.Map(
                    id='city-map',
                    style={'width': '100%', 'height': '500px'},
                    center=[49.272877, -123.078896],
                    zoom=11.2,
                )
            ], style={'marginBottom': '10px', 'border': '1px solid #ddd', 'padding': '10px'}),

            html.Div([
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[
                        {'label': loc, 'value': loc} for loc in sorted(property_values['geo_local_area'].unique())
                    ],
                    value=None,
                    placeholder='Select a Neighbourhood'
                )
            ], style={'marginBottom': '10px', 'border': '1px solid #ddd', 'padding': '10px'}),

            html.Div([
                dcc.Dropdown(
                    id='zoning-dropdown',
                    options=[
                        {'label': loc, 'value': loc} for loc in sorted(property_values['zoning_classification'].unique())
                    ],
                    value=None,
                    placeholder='Select a Zoning Type'
                )
            ], style={'border': '1px solid #ddd', 'padding': '10px'}) 
        ], style={'width': '65%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px', 'backgroundColor': '#f0f8ff'}),

        # Row 2: Charts (Right Column)
        html.Div([
            html.Div([
                html.Iframe(
                    id='pie-chart',
                    style={'width': '100%', 'height': '400px', 'border': 'none'}
                )
            ], style={'marginBottom': '10px', 'border': '1px solid #ddd', 'padding': '10px'}), 

            html.Div([
                html.Iframe(
                    id='bar-chart',
                    style={'width': '100%', 'height': '300px', 'border': 'none'}
                )
            ], style={'marginBottom': '10px', 'border': '1px solid #ddd', 'padding': '10px'}), 

            html.Div([
                html.Iframe(
                    id='scatter-plot',
                    style={'width': '100%', 'height': '400px', 'border': 'none'}
                )
            ], style={'border': '1px solid #ddd', 'padding': '10px'}) 
        ], style={'width': '35%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px', 'backgroundColor': '#fff8dc'}),
    ], style={'display': 'flex', 'justifyContent': 'flex-start', 'alignItems': 'flex-start', 'gap': '20px'}),
])

# Register callbacks
register_map_callbacks(app, issues_values_joined)
register_chart_callbacks(app, issues, issues_values_joined, property_values)

# Run the app
if __name__ == '__main__':
    app.server.run(host='127.0.0.1', port=8050)
