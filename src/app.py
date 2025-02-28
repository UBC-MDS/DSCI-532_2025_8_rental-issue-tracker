from dash import Dash, dcc, html
import altair as alt
import pandas as pd
from dash.dependencies import Input, Output

# Sample data for pie chart
data = pd.DataFrame({
    'Location': ['Downtown', 'Hastings-Sunrise', 'Kitsilano', 'Marpole', 'Grandview-Woodland', 'Other'],
    'Issues': [100, 150, 200, 250, 300, 350]
})

# Load data for bar chart
df = pd.read_csv('data/clean/rentals_with_property_value.csv')

def create_pie_chart(data):
    chart = alt.Chart(data, title='Number of Rental Issues').mark_arc().encode(
        theta=alt.Theta('Issues', type='quantitative'),
        color=alt.Color('Location', type='nominal'),
        tooltip=['Location', 'Issues']
    ).properties(
        width=400,
        height=400
    )
    return chart

# Create horizontal bar chart function
def create_bar_chart(data, x_col, y_col, title, x_title=None, y_title=None):
    if x_title is None:
        x_title = x_col
    if y_title is None:
        y_title = y_col

    chart = alt.Chart(data).mark_bar().encode(
        y=alt.Y(y_col, title=y_title),
        x=alt.X(x_col, title=x_title),
        tooltip=[y_col, x_col]
    ).properties(
        title=title
    ).interactive()
    return chart

# Create scatter plot
def create_scatter_plot(data, x_col, y_col, tooltip, title, x_title=None, y_title=None):
    if x_title is None:
        x_title = x_col
    if y_title is None:
        y_title = y_col
    
    points = alt.Chart(data).mark_point().encode(
        y=alt.Y(y_col, title=y_title),
        x=alt.X(x_col, title=x_title),
        tooltip=[tooltip]
    )

    fit_line = points.transform_regression(x_col, y_col).mark_line()

    chart = (points + fit_line).properties(
        title=title
    ).interactive()

    return chart

# Initialize the app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    # TODO: add map here
    html.Div([
        
    ], style={'width': '50%', 'display': 'inline-block'}),
    
    html.Div([
        # TODO: add pie chart here
        html.Iframe(
            id='pie-chart',
            style={'width': '100%', 'height': '200px', 'border': 'none'}
        ),

        # Bar chart
        html.Iframe(
            id='bar-chart',
            style={'width': '100%', 'height': '200px', 'border': 'none'}
        ),

        # Scatter plot
        html.Iframe(
            id='scatter-plot',
            style={'width': '100%', 'height': '300px', 'border': 'none'}
        )
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

    html.Div([
        html.Label('Select a Region:'),
        dcc.Dropdown(
            id='region-dropdown',
            options=[
                {'label': loc, 'value': loc} for loc in df['geo_local_area'].unique()
            ],
            value=df['geo_local_area'].unique()[0] if df['geo_local_area'].unique().size > 0 else None
        )
    ], style={'width': '100%', 'padding': '20px', 'display': 'block'})
], style={'width': '100%'})

# Callback for pie chart
@app.callback(
    Output('pie-chart', 'srcDoc'),
    Input('pie-chart', 'id')
)
def update_pie_chart(id):
    return create_pie_chart(data).to_html()

# Callback for bar chart (Global view)
@app.callback(
    Output('bar-chart', 'srcDoc'),
    Input('region-dropdown', 'value')
)
def update_bar_chart(selected_region):
    if selected_region:
        filtered_df = df[df['geo_local_area'] == selected_region]
        aggregated_df = filtered_df.groupby('zoning_classification')['total_outstanding'].sum().reset_index()
    else:
        aggregated_df = df.groupby('zoning_classification')['total_outstanding'].sum().reset_index()

    chart = create_bar_chart(
        data=aggregated_df,
        x_col='total_outstanding',
        y_col='zoning_classification',
        title='Total Outstanding Issues by Zoning Classification',
        x_title='Total Outstanding Issues',
        y_title='Zoning Classification'
    )
    return chart.to_html()

# Callback for scatter plot
@app.callback(
    Output('scatter-plot', 'srcDoc'),
    Input('region-dropdown', 'value')
)
def update_scatter_plot(selected_region):
    if selected_region:
        filtered_df = df[df['geo_local_area'] == selected_region]
    else:
        filtered_df = df

    chart = create_scatter_plot(
        data=filtered_df,
        x_col='current_land_value',
        y_col='total_outstanding',
        tooltip='geo_local_area',
        title='Property Prices vs Outstanding Issues',
        x_title='Property Prices',
        y_title='Outstanding Issues'
    )
    return chart.to_html()

# Run the app/dashboard
if __name__ == '__main__':
    app.server.run(debug=True, host='127.0.0.1', port=8050)