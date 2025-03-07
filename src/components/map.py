import dash_leaflet as dl
import pandas as pd
from ..data.data import load_data, zone_icon_dict

issues_values_joined, property_values, issues = load_data()

def create_map_icon(row):
    '''
    Given a row from the dataframe, create an icon with tooltip info on map.
    '''
    property_value = 'N/A' if pd.isna(row['current_land_value']) else f"${row['current_land_value']:,.2f}"
    
    
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
