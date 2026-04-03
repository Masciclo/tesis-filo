import sys
from pathlib import Path

# Asegurar que la carpeta raíz del proyecto esté en el path de búsqueda de módulos
this_file = Path(__file__).resolve()
project_root = this_file.parents[1]
sys.path.append(str(project_root))  # permite importar config.py

# Ahora podemos importar la configuración de rutas
def load_data_and_plot():
    from config import DATA_DIR
    import pandas as pd
    import plotly.express as px

    # Ruta al CSV usando pathlib
    csv_path = DATA_DIR / 'WUP2018-F11b-30_Largest_Cities_in_2018_by_time_delimitado.csv'
    df = pd.read_csv(csv_path, sep=';', engine='python', decimal=',')

    # Definir años de interés
    years_20 = [1950, 1970, 1990, 2010, 2030]
    df_20 = df[df['Year'].isin(years_20)]

    # Pivot y cálculo de tasas
    pivot_df = df_20.pivot_table(
        index='Urban Agglomeration',
        columns='Year',
        values='Population (millions)'
    ).reset_index()
    pivot_df['1950-1970'] = (pivot_df[1970] - pivot_df[1950]) / pivot_df[1950]
    pivot_df['1970-1990'] = (pivot_df[1990] - pivot_df[1970]) / pivot_df[1970]
    pivot_df['1990-2010'] = (pivot_df[2010] - pivot_df[1990]) / pivot_df[1990]
    pivot_df['2010-2030'] = (pivot_df[2030] - pivot_df[2010]) / pivot_df[2010]

    # Calcular tasa media
    pivot_df['Mean Growth Rate'] = pivot_df[
        ['1950-1970','1970-1990','1990-2010','2010-2030']
    ].mean(axis=1)
    growth_df = pivot_df.sort_values(by='Mean Growth Rate', ascending=False)

    # Determinar top 5 ciudades
    top5 = growth_df['Urban Agglomeration'].head(5).tolist()
    df['color_group'] = df['Urban Agglomeration'].apply(
        lambda city: city if city in top5 else 'Otras'
    )

    # Use Turbo color scale for mapping explicit colors
    turbo_colors = px.colors.sample_colorscale('turbo', [0.1, 0.3, 0.5, 0.7, 0.9])
    color_map = {city: turbo_colors[i] for i, city in enumerate(top5)}
    color_map['Otras'] = '#cccccc'

    # Crear gráfico
    fig = px.line(
        df,
        x='Year',
        y='Population (millions)',
        color='color_group',
        line_group='Urban Agglomeration',
        color_discrete_map=color_map,
        labels={
            'Year': 'Año',
            'Population (millions)': 'Población (millones)',
            'color_group': 'Ciudad (Top 5 u Otras)'
        },
        title='Evolución de la población por ciudad (solo Top 5 ciudades destacadas)'
    )

    return fig

# Ejecutar la función y mostrar la figura si se ejecuta directamente
if __name__ == '__main__':
    fig = load_data_and_plot()
    fig.show()
else:
    # En Quarto/Jupyter, dejar fig como último objeto
    fig = load_data_and_plot()
    fig
