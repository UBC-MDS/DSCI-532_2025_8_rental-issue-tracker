from dash import Dash, dcc, html
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash_vega_components import Vega
from .data.data import load_data
from .callbacks.map import register_map_callbacks
from .callbacks.charts import register_chart_callbacks
from .components.charts import create_bar_chart

# Load data
issues_values_joined, property_values, issues, area_boundaries = load_data()

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Create initial bar chart specification
initial_bar_spec = create_bar_chart(
    data=issues_values_joined.groupby('zoning_classification')['total_outstanding'].sum().reset_index(),
    x_col='total_outstanding',
    y_col='zoning_classification',
    title='Total Outstanding Issues by Zoning Classification',
    x_title='Total Outstanding Issues',
    y_title='Zoning Classification'
)

# Layout
app.layout = dbc.Container([

    # Title Section
    dbc.Row(
        dbc.Col(
            html.H1("Vancouver Rental Issue Tracker Dashboard", 
                    style={'textAlign': 'center', 'marginBottom': '20px'}),
            width=12
        ),
        style={'width': '100%', 'padding': '10px', 'backgroundColor': '#f9f9f9', 
               'margin': '0 auto'}
    ),

    # Main Content Section (Grid Layout)
    dbc.Row([
        # Left Column
        dbc.Col([
            dbc.Card(
                dl.Map(
                    id='city-map',
                    style={'height': '400px'},
                    center=[49.272877, -123.078896],
                    zoom=11.2,
                ),
                style={'marginBottom': '10px', 'border': '1px solid #ddd', 'padding': '10px'}
            ),

            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dcc.Dropdown(
                            id='region-dropdown',
                            options=[
                                {'label': loc, 'value': loc} for loc in sorted(property_values['geo_local_area'].unique())
                            ],
                            value=None,
                            placeholder='Select a Neighbourhood'
                        ),
                    style={'height': '100%', 'border': '1px solid #ddd', 'padding': '10px'}
                    ),
                    width=6
                ),

                dbc.Col(
                    dbc.Card(
                        dcc.Dropdown(
                            id='zoning-dropdown',
                            options=[
                            {'label': loc, 'value': loc} for loc in sorted(property_values['zoning_classification'].unique())
                            ],
                            value=None,
                            placeholder='Select a Zoning Type'
                        ),
                    style={'height': '100%', 'border': '1px solid #ddd', 'padding': '10px'}
                    ),
                    width=6
                ),
            ], className="mb-3"),

            dbc.Card(
                Vega(
                    id='bar-chart',
                    spec=initial_bar_spec,
                    style={'width': '100%', 'height': '230px'}
                ),
                style={'marginBottom': '10px', 'border': '1px solid #ddd', 'padding': '10px'}
            )

        ], width=7, style={'padding': '10px', 'backgroundColor': '#f0f8ff'}),

        # Right Column
        dbc.Col([
            dbc.Card(
                html.Iframe(
                    id='pie-chart',
                    style={'width': '100%', 'height': '350px', 'border': 'none'}
                ),
                style={'marginBottom': '10px', 'border': '1px solid #ddd', 'padding': '10px'}
            ),

            dbc.Card(
                dbc.CardBody([
                    html.Iframe(
                    id='scatter-plot',
                    style={'width': '100%', 'height': '292px', 'border': 'none'}
                    ),
                dcc.RadioItems(
                    id='scale-radio',
                    options=[
                    {'label': 'Linear', 'value': 'linear'},
                    {'label': 'Logarithmic', 'value': 'log'},
                    ],
                    value='linear',
                    inline=True,
                    style={'display': 'flex', 'gap': '15px'}
                    )   
                ]),
                style={'border': '1px solid #ddd', 'padding': '10px'}
            ),
        ], style={'padding': '10px', 'backgroundColor': '#fff8dc'}),
    ]),

    # Footer Section (Description)
    dbc.Row(
        dbc.Col([
            html.P(
                "This dashboard combines rental property by-law issues with property tax data from the Vancouver Open Data portal. "
                "It helps users identify trends, pinpoint high-risk properties, explore the connection between property violations and tax assessments, "
                "and estimate rental costs.",
                style={'fontSize': '14px', 'marginBottom': '10px', 'color': '#333'}
            ),
            html.P(
                "Developed by Group 8 | Last updated: 3/7/2025",
                style={'fontSize': '12px', 'marginBottom': '10px', 'color': '#666'}
            ),
            html.A(
                "View on GitHub",
                href="https://github.com/UBC-MDS/DSCI-532_2025_8_rental-issue-tracker",
                target="_blank",
                style={'fontSize': '12px', 'color': '#007bff', 'textDecoration': 'underline'}
            )
        ], width=12),
        style={'width': '100%', 'padding': '10px', 'textAlign': 'center', 'backgroundColor': '#f9f9f9', 'marginTop': '20px'}
    )
], fluid=True)

# Register callbacks
register_map_callbacks(app, issues_values_joined)
register_chart_callbacks(app, issues, issues_values_joined, property_values)

# Run the app
if __name__ == '__main__':
    app.server.run(host='127.0.0.1', port=8050)