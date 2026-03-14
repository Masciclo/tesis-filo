import geopandas as gpd
import pandas as pd
import plotly.express as px
import numpy as np

# 1) Load & subset your GeoDataFrame
gdf = gpd.read_file(
    "C:/Users/Javiera/Desktop/Libro jupyter book/tesis-filo/data/merged_urban_natural_earth.geojson"
)
year_columns = ['1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020','2030',]
gdf_filtered = gdf[['Country', 'ISO_A3'] + year_columns].copy()

# 2) Clean & convert comma→dot floats if needed
for yr in year_columns:
    gdf_filtered[yr] = (
        gdf_filtered[yr]
        .astype(str)
        .str.replace(',', '.', regex=False)
        .pipe(pd.to_numeric, errors='coerce')
    )

# 3) Melt to long form
df_long = gdf_filtered.melt(
    id_vars=['ISO_A3', 'Country'],
    value_vars=year_columns,
    var_name='Year',
    value_name='Percent'
)

# 4) Build the choropleth with slider
fig = px.choropleth(
    df_long,
    locations='ISO_A3',          # ISO-3 codes for mapping
    color='Percent',             # percent values
    locationmode='ISO-3',
    animation_frame='Year',      # slider over Year
    range_color=(0, 100),        # fixed color range
    color_continuous_scale='Portland_r',
    scope='world',
    hover_name='Country',        
    hover_data={'Percent': ':.2f'},  
    marker_line_width=0          # ✅ remove country borders
)

# 5) Clean layout and appearance
fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        showcountries=False,
        bgcolor="white",
        landcolor="white"
    ),
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=0, r=0, t=30, b=0),
    transition=dict(duration=500)  # Optional: smooth animation transitions
)

# 6) Show the figure
fig.show()


gdf.columns