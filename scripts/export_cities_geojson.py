import sys
import json
import pandas as pd
from pathlib import Path

# Add project root to sys path to import config
this_file = Path(__file__).resolve()
project_root = this_file.parents[1]
sys.path.append(str(project_root))

from config import DATA_DIR

def load_data_and_export_geojson():
    csv_path = DATA_DIR / 'WUP2025-F18-DEGURBA-100_Largest_Cities.csv'
    df = pd.read_csv(csv_path, sep=';', encoding='latin1', engine='python')

    features = []
    cities = df['City_Name'].unique()
    all_years = df['Year'].dropna().unique()

    for city in cities:
        city_df = df[df['City_Name'] == city]
        
        # Geolocation string cleanup in case they have commas
        lat_str = str(city_df['PWCent_Latitude'].iloc[0]).replace(',', '.')
        lon_str = str(city_df['PWCent_Longitude'].iloc[0]).replace(',', '.')
        lat = float(lat_str)
        lon = float(lon_str)
        
        # Populate each year, defaulting to 0.0 for undefined/missing 
        pops = {f'pop_{y}': 0.0 for y in all_years}
        for _, row in city_df.iterrows():
            if not pd.isna(row['Population']):
                year = str(row['Year'])
                try:
                    pop_val = float(str(row['Population']).replace(',', '.'))
                    pops[f'pop_{year}'] = pop_val
                except ValueError:
                    pass
        
        properties = {
            'name': city,
        }
        properties.update(pops)
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": properties
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    output_path = DATA_DIR / 'cities_development.geojson'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"Bake completed: Exported {len(cities)} cities geojson to {output_path}")

if __name__ == '__main__':
    load_data_and_export_geojson()
