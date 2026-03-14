import geopandas as gpd
import pandas as pd
import plotly.express as px
import numpy as np

# 1) Load & subset your GeoDataFrame
gdf = gpd.read_file(
    "C:/Users/Javiera/Desktop/Libro jupyter book/tesis-filo/data/merged_urban_natural_earth.geojson"
)
year_columns = ['1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020','2025']
gdf_filtered = gdf[['Country', 'ISO_A3'] + year_columns].copy()

# 2) Clean & convert comma→dot floats if needed
for yr in year_columns:
    gdf_filtered[yr] = (
        gdf_filtered[yr]
        .astype(str)
        .str.replace(',', '.', regex=False)
        .pipe(pd.to_numeric, errors='coerce')
    )

mean_values = gdf_filtered[year_columns].mean()
print(mean_values)


print(gdf_filtered['Country'].to_list())

country_row = gdf_filtered[gdf_filtered['Country'] == 'United States of America']
print(country_row)
country_row = gdf_filtered[gdf_filtered['Country'] == 'Chile']
print(country_row)
country_row = gdf_filtered[gdf_filtered['Country'] == 'Germany']
print(country_row)
country_row = gdf_filtered[gdf_filtered['Country'] == 'China']
print(country_row)