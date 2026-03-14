import geopandas as gpd
import pandas as pd
import plotly.express as px
import numpy as np
import json

# 1) Load & subset your GeoDataFrame
gdf = gpd.read_file("C:/Users/Javiera/Desktop/Libro jupyter book/tesis-filo/data/merged_urban_natural_earth.geojson")
year_columns = ['1950', '1970', '1990', '2010', '2025']
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
    locations='ISO_A3',          
    color='Percent',             
    locationmode='ISO-3',
    animation_frame='Year',      
    range_color=(0, 100),        
    color_continuous_scale='Aggrnyl_r',
    scope='world',
    hover_name='Country',        
    hover_data={'Percent': ':.2f'}
)

fig.update_traces(colorbar_showscale=False)
fig.update_layout(
    margin={'r':0, 't':40, 'l':0, 'b':0},
    title='Global Urban Population (%) by Country (1950–2025)'
)

# 5) Save the map to HTML
html_file = "urbanization_map.html"
fig.write_html(html_file, include_plotlyjs='cdn')

# 6) Define your local dictionary (you can edit as needed)
dic = {
    "Country": "Country name",
    "ISO_A3": "ISO-3 country code used for mapping",
    "Year": "Year of data observation (1950 to 2025)",
    "Percent": "Estimated percentage of urban population in each country"
}

# 7) Append the dictionary as JSON inside the HTML
with open(html_file, "a", encoding="utf-8") as f:
    f.write("\n<!-- Metadata Dictionary -->\n")
    f.write("<script type='application/json' id='metadata-dict'>\n")
    json.dump(dic, f, indent=2, ensure_ascii=False)
    f.write("\n</script>\n")
