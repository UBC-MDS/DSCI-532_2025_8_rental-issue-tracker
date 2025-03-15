import pandas as pd
import pickle as pckl
import functools

def process_and_save_data():
    # Load data
    property_values = pd.read_parquet('data/clean/rentals_with_property_value.parquet')
    issues = pd.read_parquet('data/clean/rental_issues_clean.parquet')

    # Process the data
    issues_values_joined = pd.merge(issues, property_values, how='left').drop_duplicates(subset=['lat', 'long'])
    issues_values_joined['zoning_classification'] = (
        issues_values_joined['zoning_classification'].astype(str).replace("nan", "N/A")
    )

    # Load and process boundary data
    with open('data/raw/local-area-boundary.pkl', 'rb') as file:
        area_boundaries = pckl.load(file)

    # Get sorted neighborhoods
    neighborhoods = sorted(issues_values_joined['geo_local_area'].unique().tolist())

    # Create boundary index
    boundary_index = {entry['properties']['name']:i for i,entry in enumerate(area_boundaries['features'])}
    del boundary_index['Oakridge']

    # Create style dictionary
    style_dictionary = {}
    for neighborhood in boundary_index.keys():
        color = neighborhood_color_range[neighborhoods.index(neighborhood)]
        style_dictionary.update({
            neighborhood:{
                "fillColor": color,
                "color": "black",
                "weight": 2,  
                "fillOpacity": 0.5
            }
        })

    # Save processed data
    processed_data = {
        'issues_values_joined': issues_values_joined,
        'property_values': property_values,
        'issues': issues,
        'area_boundaries': area_boundaries,
        'neighborhoods': neighborhoods,
        'boundary_index': boundary_index,
        'style_dictionary': style_dictionary
    }
    
    with open('data/processed/processed_data.pkl', 'wb') as f:
        pckl.dump(processed_data, f)

@functools.lru_cache()
def load_data():
    with open('data/processed/processed_data.pkl', 'rb') as f:
        data = pckl.load(f)
    return (
        data['issues_values_joined'],
        data['property_values'],
        data['issues'],
        data['area_boundaries'],
        data['neighborhoods'],
        data['boundary_index'],
        data['style_dictionary']
    )

# Constants
zone_icon_dict = {
    'Commercial':('#2A81CB','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png'),
    'Historical Area':('#CB2B3E','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png'),
    'Industrial':('#2AAD27','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png'),
    'Residential':('#FFD326	','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png'),
    'Residential Inclusive':('#9C2BCB','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-violet.png'),
    'N/A':('#7B7B7B','https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-grey.png')
}

geo_location_dict = {
    'Arbutus Ridge':{'zoom':13.87,'center':[49.2467288,-123.1594228]},
    'Downtown':{'zoom':13.87,'center':[49.2790925,-123.1147099]},
    'Dunbar-Southlands':{'zoom':12.9,'center':[49.234845, -123.185501]},
    'Fairview':{'zoom':14.37,'center':[49.2654975,-123.1282056]},
    'Grandview-Woodland':{'zoom':13.5,'center':[49.2759762,-123.0682878]},
    'Hastings-Sunrise':{'zoom':13,'center':[49.2778156,-123.0422014]},
    'Kensington-Cedar Cottage':{'zoom':13.5,'center':[49.2471833,-123.0769395]},#
    'Killarney':{'zoom':13.5,'center':[49.2180367,-123.0383941]},#
    'Kitsilano':{'zoom':13.5,'center':[49.2674605,-123.1642213]},#
    'Marpole':{'zoom':14,'center':[49.2104717,-123.130635]},#
    'Mount Pleasant':{'zoom':14,'center':[49.2647148,-123.0978001]},#
    'Renfrew-Collingwood':{'zoom':13.2,'center':[49.2483732,-123.0386256]},#
    'Riley Park':{'zoom':13.8,'center':[49.24452,-123.1020171]},#
    'Shaughnessy':{'zoom':13.8,'center':[49.2456008,-123.1415797]},#
    'Strathcona':{'zoom':13.6,'center':[49.276685, -123.089812]},
    'Sunset':{'zoom':13.6,'center':[49.2188485,-123.0911351]},
    'West End':{'zoom':14.31,'center':[49.2853688,-123.1342539]}
}

neighborhood_color_range = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5',
    '#fd8b3c'
]

# Run only once
# process_and_save_data()
