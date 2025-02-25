from dash import Dash, dcc, html
import altair as alt
import pandas as pd
from dash.dependencies import Input, Output

# Sample data for pie chart
data = pd.DataFrame({
    'Location': ['Downtown', 'Hastings-Sunrise', 'Kitsilano', 'Marpole', 'Grandview-Woodland', 'Other'],
    'Issues': [100, 150, 200, 250, 300, 350]
})

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

# Load data for bar chart
df = pd.read_csv('data/clean/rentals_with_property_value.csv')

# Create horizontal bar chart function
def create_bar_chart(data, x_col, y_col, title, x_title=None, y_title=None):
    """
    Creates a horizontal bar chart using Altair.

    Args:
        data (pd.DataFrame): The data source for the chart.
        x_col (str): The column name to be used for the x-axis (horizontal axis).
        y_col (str): The column name to be used for the y-axis (vertical axis).
        title (str): The title of the chart.
        x_title (str, optional): Custom title for the x-axis. Defaults to None, which uses x_col as the title.
        y_title (str, optional): Custom title for the y-axis. Defaults to None, which uses y_col as the title.

    Returns:
        alt.Chart: An Altair chart object representing the bar chart.
    """
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

# Initialize the app
app = Dash(__name__)

# Layout - includes pie and bar charts
app.layout = html.Div([
    html.Div([
        html.Iframe(
            id='pie-chart',
            height='500',
            width='500',
            style={'border-width': '0'}
        )
    ], style={'width': '30%', 'display': 'inline-block'}),

    # Bar chart Iframe
    html.Div([
        html.Iframe(
            id='bar-chart',
            height='500',
            width='700',
            style={'border-width': '0'}
        )
    ], style={'width': '70%', 'display': 'inline-block', 'vertical-align': 'top'}),

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
    aggregated_df = df.groupby('zoning_classification')['total_outstanding'].sum().reset_index()

    chart = create_bar_chart(
        data=aggregated_df,
        x_col='total_outstanding',
        y_col='zoning_classification',
        title='Total Outstanding Issues by Zoning Classification (Global)',
        x_title='Total Outstanding Issues',
        y_title='Zoning Classification'
    )
    return chart.to_html()

# Run the app/dashboard
if __name__ == '__main__':
    app.server.run(debug=True, host='127.0.0.1', port=8050)