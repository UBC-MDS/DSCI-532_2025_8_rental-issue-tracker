from dash.dependencies import Input, Output
from ..common.extensions import cache
import dash_leaflet as dl
from ..components.map import create_map_icons,get_geo_style
from ..data.data import load_data, geo_location_dict

issues_values_joined, property_values, issues, area_boundaries, neighborhoods, boundary_index, style_dictionary = load_data()

def register_map_callbacks(app, issues_values_joined):
    # Callback for map
    @app.callback(
        Output('city-map', 'viewport'),
        Output('city-map', 'children'),
        Input('region-dropdown', 'value'),
        Input('zoning-dropdown','value'),
        Input('na-button','n_clicks')
    )
    @cache.memoize()
    def update_map(selected_region, selected_zone,n_clicks):    
        """Updates the map view based on selected region and zone filters."""
        # Function implementation...
        # Default center and zoom
        geo_data = area_boundaries.copy()
        icon_data = issues_values_joined.copy()
        center = [49.252548, -123.100777]  # Default center
        zoom = 11.6  # Default zoom
        style = {
        "fillColor": 'grey',
        "color": "black",
        "weight": 2,  
        "fillOpacity": 0.2
        } # default style
        remove_na = bool(n_clicks % 2)
        
        # remove N/A values if button clicked
        if remove_na:
            icon_data = icon_data[~icon_data['zoning_classification'].str.contains('N/A')]
        
        # zoom to selected neighborhood
        if selected_region:
            center = geo_location_dict[selected_region]['center']
            zoom = geo_location_dict[selected_region]['zoom']
            geo_data = area_boundaries['features'][boundary_index[selected_region]]
            style = style_dictionary[selected_region]
        
        # Apply zoning filter
        if selected_zone:
            icon_data = icon_data[icon_data['zoning_classification'] == selected_zone]
        
        # dont add icons if no 
        if icon_data.empty:
            children = [
                dl.TileLayer(), 
                dl.GeoJSON(
                    data=geo_data,
                    style=style
                ),
            ]
        else:
            children = [
                dl.TileLayer(), 
                dl.GeoJSON(
                    data=geo_data,
                    style=style
                ),
                *create_map_icons(icon_data)
            ]
        
        if selected_zone and isinstance(selected_zone, str):
            icon_data = icon_data[icon_data['zoning_classification'].str.contains(selected_zone, na=False)]
        else:
            icon_data = icon_data.copy()        

        # Return the updated center, zoom, and children (markers)
        return {'center':center, 'zoom':zoom,'transition':"flyTo"}, children