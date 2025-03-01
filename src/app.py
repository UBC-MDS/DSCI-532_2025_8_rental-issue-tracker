from dash import Dash, dcc, html
import altair as alt
import pandas as pd
from dash.dependencies import Input, Output
import dash_leaflet as dl

property_values = pd.read_csv('data/clean/rentals_with_property_value.csv',index_col=0)
issues = pd.read_csv('data/clean/rental_issues_clean.csv',index_col=0)

# left join two dataframes above
issues_values_joined = pd.merge(issues,property_values,how='left').drop_duplicates(subset=['lat','long'])
issues_values_joined['zoning_classification'] = issues_values_joined['zoning_classification'].astype(str).replace("nan", "N/A")


# dictionary that maps zoning classes to icon colors
zone_icon_dict = {
    'Commercial':('blue','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png'),
    'Historical Area':('red','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png'),
    'Industrial':('green','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png'),
    'Residential':('yellow','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png'),
    'Residential Inclusive':('purple','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-violet.png'),
    'N/A':('grey','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-grey.png')
}

# dictionary that gives locations of neighborhoods on map
geo_location_dict = {
    'Arbutus Ridge':{'zoom':14.17,'center':[49.2467288,-123.1594228]},
    'Downtown':{'zoom':14.54,'center':[49.2790925,-123.1147099]},
    'Dunbar-Southlands':{'zoom':14.02,'center':[49.2489659,-123.1860719]},
    'Fairview':{'zoom':14.37,'center':[49.2654975,-123.1282056]},
    'Grandview-Woodland':{'zoom':13.91,'center':[49.2759762,-123.0682878]},
    'Hastings-Sunrise':{'zoom':13,'center':[49.2778156,-123.0422014]},
    'Kensington-Cedar Cottage':{'zoom':14.01,'center':[49.2471833,-123.0769395]},
    'Killarney':{'zoom':13.78,'center':[49.2180367,-123.0383941]},
    'Kitsilano':{'zoom':14.26,'center':[49.2674605,-123.1642213]},
    'Marpole':{'zoom':14.46,'center':[49.2104717,-123.130635]},
    'Mount Pleasant':{'zoom':14.63,'center':[49.2647148,-123.0978001]},
    'Renfrew-Collingwood':{'zoom':13.81,'center':[49.2483732,-123.0386256]},
    'Riley Park':{'zoom':14.28,'center':[49.24452,-123.1020171]},
    'Shaughnessy':{'zoom':14.3,'center':[49.2456008,-123.1415797]},
    'Strathcona':{'zoom':14.94,'center':[49.2725961,-123.0887926]},
    'Sunset':{'zoom':14.08,'center':[49.2188485,-123.0911351]},
    'West End':{'zoom':14.71,'center':[49.2853688,-123.1342539]}
}

def create_map_icon(row):
    '''
    Given a row from the dataframe, create an icon with tooltip info on map.
    '''
    property_value = 'N/A' if pd.isna(row['current_land_value']) else f'${row['current_land_value']:,.2f}'
    
    
    content = f"""
    Operator: {row['business_operator']}<br>
    Address: {row['street_number']} {row['street']}<br>
    Zoning Type: {row['zoning_classification']}<br>
    Units: {row['total_units']}<br>
    Value: {property_value}<br>
    <b>Issues:<b/> {row['total_outstanding']}    
    """
    
    # get icon position and color
    lat = row['lat']
    long = row['long']
    zoning_class = row['zoning_classification']
    icon_url = zone_icon_dict[zoning_class][1]
    id = int(row.name) # id for each marker
    
    return dl.Marker(
        id=str(id),
        position=[lat,long],
        children=[dl.Tooltip(content=content)],
        icon={'iconUrl':icon_url}
    )

def create_map_icons(data):
    '''
    Return a list of map icons given data
    '''
    return data.apply(create_map_icon,axis=1).to_list()

def create_pie_chart(data, selected_region):

    base = alt.Chart(data, title='Number of Rental Issues').mark_arc().encode(
        theta=alt.Theta('total_outstanding', type='quantitative'),
        tooltip=['geo_local_area', 'total_outstanding'],
        order=alt.Order('total_outstanding:Q', sort='descending')
    )

    if selected_region is not None:
        chart = base.encode(
            color=alt.condition(
                alt.datum.geo_local_area == selected_region,
                alt.Color('geo_local_area:N', title='Local Area'),
                alt.value('gray'),
            ),
            opacity=alt.condition(
                alt.datum.geo_local_area == selected_region,
                alt.value(1.0),
                alt.value(0.2)
            )
        )
    else:
        # If no selected_location, use full color for all
        chart = base.encode(
            color=alt.Color('geo_local_area:N', title='Local Area')
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
        # Map
        dl.Map(
            id='city-map',
            style={'width': '100%', 'height': '400px'},
            children=[
                dl.TileLayer(),
                *create_map_icons(property_values)
            ],
            center=[49.272877, -123.078896],
            zoom=11.2,
        ),
        html.Label('Select a Region:'),
        dcc.Dropdown(
            id='region-dropdown',
            options=[
                {'label': loc, 'value': loc} for loc in sorted(property_values['geo_local_area'].unique())
            ],
            value=None
        ),
        html.Label('Select a Building Type:'),
        dcc.Dropdown(
            id='zoning-dropdown',
            options=[
                {'label': loc, 'value': loc} for loc in sorted(property_values['zoning_classification'].unique())
            ],
            value=None
        )
    ], style={'width': '50%', 'display': 'inline-block'}),
    
    html.Div([
        # TODO: add pie chart here
        html.Iframe(
            id='pie-chart',
            style={'width': '100%', 'height': '400px', 'border': 'none'}
        ),

        # Bar chart
        html.Iframe(
            id='bar-chart',
            style={'width': '100%', 'height': '300px', 'border': 'none'}
        ),

        # Scatter plot
        html.Iframe(
            id='scatter-plot',
            style={'width': '100%', 'height': '400px', 'border': 'none'}
        )
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

    html.Div([
        # TODO: update dropdown list with actual region values
        
    ], style={'width': '100%', 'padding': '20px', 'display': 'block'})
], style={'width': '100%'})

# Callback for map
@app.callback(
    Output('city-map', 'viewport'),
    Output('city-map', 'children'),
    Input('region-dropdown', 'value'),
    Input('zoning-dropdown','value')
)
def update_map(selected_region, selected_zone):    
    # Default center and zoom
    icon_data = issues_values_joined.copy()
    center = [49.272877, -123.078896]  # Default center
    zoom = 11.2  # Default zoom
    
    # zoom to selected neighborhood
    if selected_region:
        center = geo_location_dict[selected_region]['center']
        zoom = geo_location_dict[selected_region]['zoom']
    
    # Apply zoning filter
    if selected_zone:
        icon_data = icon_data[icon_data['zoning_classification'] == selected_zone]
    
    children = [
        dl.TileLayer(),  
        *create_map_icons(icon_data)
    ]
    
    # Return the updated center, zoom, and children (markers)
    return {'center':center, 'zoom':zoom,'transition':"flyTo"}, children
      
# Callback for pie chart
@app.callback(
    Output('pie-chart', 'srcDoc'),
    Input('region-dropdown', 'value')
)
def update_pie_chart(selected_region):
    aggregated_property_values = issues.groupby('geo_local_area')['total_outstanding'].sum().reset_index()
    return create_pie_chart(aggregated_property_values, selected_region).to_html()

# Callback for bar chart (Global view)
@app.callback(
    Output('bar-chart', 'srcDoc'),
    Input('region-dropdown', 'value')
)
def update_bar_chart(selected_region):
    if selected_region:
        filtered_property_values = issues_values_joined[issues_values_joined['geo_local_area'] == selected_region]
        aggregated_property_values = filtered_property_values.groupby('zoning_classification')['total_outstanding'].sum().reset_index()
    else:
        aggregated_property_values = issues_values_joined.groupby('zoning_classification')['total_outstanding'].sum().reset_index()

    chart = create_bar_chart(
        data=aggregated_property_values,
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
        filtered_property_values = property_values[property_values['geo_local_area'] == selected_region]
    else:
        filtered_property_values = property_values

    chart = create_scatter_plot(
        data=filtered_property_values,
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