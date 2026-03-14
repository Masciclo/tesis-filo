# merge_on_iso_a3.py

import pandas as pd
import geopandas as gpd

# Rutas a los archivos
CSV_PATH      = "C:/Users/Javiera/Desktop/Libro jupyter book/tesis-filo/data/WUP2018-F02-Proportion_Urban.csv"
GEOJSON_PATH  = "C:/Users/Javiera/Desktop/Libro jupyter book/tesis-filo/data/natural_earth.geojson"
OUTPUT_PATH   = "C:/Users/Javiera/Desktop/Libro jupyter book/tesis-filo/data/merged_urban_natural_earth.geojson"

def main():
    # 1. Cargar el CSV (delimitado por ;)
    df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8-sig', engine='python')

    # 2. Verificar que exista ISO_A3 en el CSV
    if 'ISO_A3' not in df.columns:
        raise KeyError("La columna 'ISO_A3' no existe en el CSV")

    # 3. Seleccionar las columnas que queremos mantener
    #    Por ejemplo, todas las columnas del CSV menos la geometría
    #    o solo un subconjunto: aquí tomo Country + ISO_A3 + proporción urbana 2020
    df_merge = df[['Country', 'ISO_A3', "1950","1955","1960","1965","1970","1975","1980","1985","1990","1995","2000","2005","2010","2015","2020","2025"
]].copy()
    #df_merge.rename(columns={'2020': 'UrbanPct2020'}, inplace=True)

    # 4. Cargar el GeoJSON de Natural Earth
    gdf = gpd.read_file(GEOJSON_PATH)

    # 5. Verificar que exista ISO_A3 en el GeoDataFrame
    if 'ISO_A3' not in gdf.columns:
        raise KeyError("La columna 'ISO_A3' no existe en el GeoJSON")

    # 6. Merge sobre ISO_A3
    merged_gdf = gdf.merge(df_merge, on='ISO_A3', how='left')

    # 7. Guardar el resultado como GeoJSON
    merged_gdf.to_file(OUTPUT_PATH, driver='GeoJSON')
    print(f"Merged GeoJSON guardado en: {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
