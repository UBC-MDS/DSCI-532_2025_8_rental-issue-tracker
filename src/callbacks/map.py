from dash.dependencies import Input, Output
import dash_leaflet as dl
from ..components.map import create_map_icons
from ..data.data import geo_location_dict

def register_map_callbacks(app, issues_values_joined):
    # Callback for map
    @app.callback(
        Output('city-map', 'viewport'),
        Output('city-map', 'children'),
        Input('region-dropdown', 'value'),
        Input('zoning-dropdown','value')
    )
    def update_map(selected_region, selected_zone):    
        """Updates the map view based on selected region and zone filters."""
        # Function implementation...
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