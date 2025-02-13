from dash import Dash, dcc, html
import altair as alt
import pandas as pd
from dash.dependencies import Input, Output

# Sample data
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

# Initialize the app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.Div([
        html.Iframe(
            id='pie-chart',
            height='500',
            width='500',
            style={'border-width': '0'}
        )
    ], style={'width': '30%', 'display': 'inline-block'}),

    html.Div([
        html.Label('Select a Region:'),
        dcc.Dropdown(
            options=[
                {'label': loc, 'value': loc} for loc in data['Location']
            ],
            value='Downtown'
        )
    ], style={'width': '30%', 'padding': '20px', 'display': 'inline-block'})
])

@app.callback(
    Output('pie-chart', 'srcDoc'),
    Input('pie-chart', 'id')
)
def update_pie_chart(id):
    return create_pie_chart(data).to_html()

# Run the app/dashboard
if __name__ == '__main__':
    app.server.run(debug=True, host='127.0.0.1', port=8050)
