import pandas as pd
import pickle as pckl
import json

def load_data():
    property_values = pd.read_csv('data/clean/rentals_with_property_value.csv', index_col=0)
    issues = pd.read_csv('data/clean/rental_issues_clean.csv', index_col=0)
    
    # left join two dataframes above
    issues_values_joined = pd.merge(issues, property_values, how='left').drop_duplicates(subset=['lat', 'long'])
    issues_values_joined['zoning_classification'] = (
        issues_values_joined['zoning_classification'].astype(str).replace("nan", "N/A")
    )

    # load in area boundary data
    with open('data/raw/local-area-boundary.geojson',encoding='utf-8-sig') as file:
        area_boundaries = json.load(file)

    return issues_values_joined, property_values, issues, area_boundaries

issues_values_joined, property_values, issues, area_boundaries = load_data()

# dictionary that maps zoning classes to icon colors
zone_icon_dict = {
    'Commercial':('#2A81CB','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png'),
    'Historical Area':('#CB2B3E','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png'),
    'Industrial':('#2AAD27','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png'),
    'Residential':('#FFD326	','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png'),
    'Residential Inclusive':('#9C2BCB','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-violet.png'),
    'N/A':('#7B7B7B','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-grey.png')
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

neighborhoods = sorted(issues_values_joined['geo_local_area'].unique().tolist())
neighborhood_color_range = [
'#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
'#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
'#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
'#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
'#fd8b3c'  # Adding a 21st distinct color - orange-ish
]

# index to get boundary data for each region
boundary_index = {entry['properties']['name']:i for i,entry in enumerate(area_boundaries['features'])}