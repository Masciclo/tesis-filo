import geopandas as gpd
import pandas as pd
import json

# 1) Load your GeoDataFrame
gdf = gpd.read_file(
    "C:/Users/Javiera/Desktop/Libro jupyter book/tesis-filo/data/merged_urban_natural_earth.geojson"
)

# 2) Define columns (Removed '2030' to prevent the KeyError)
year_columns = ['1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020']
gdf_filtered = gdf[['Country', 'ISO_A3'] + year_columns].copy()

# 3) Clean & convert comma to dot floats
for yr in year_columns:
    gdf_filtered[yr] = (
        gdf_filtered[yr]
        .astype(str)
        .str.replace(',', '.', regex=False)
        .pipe(pd.to_numeric, errors='coerce')
    )

# 4) Prepare for JSON export: Fill NaNs so JSON doesn't break
export_df = gdf_filtered.set_index('ISO_A3')[year_columns].fillna(-1)

# Drop any duplicate indices (e.g., country code '-99' appearing multiple times in Natural Earth data)
export_df = export_df[~export_df.index.duplicated(keep='first')]

# 5) Convert to a nested dictionary
data_dict = export_df.to_dict(orient='index')

# 6) Save directly to your Quarto project folder
output_path = "C:/Users/Javiera/Desktop/Libro jupyter book/tesis-filo/urban_data.json"
with open(output_path, "w") as f:
    json.dump(data_dict, f)

print(f"Success! Map data exported to: {output_path}")