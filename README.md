# Tesis Filo - Proyecto Quarto Book

Este repositorio contiene el código fuente, los datos y los scripts de análisis espacial que componen el libro digital interactivo creado con [Quarto](https://quarto.org/). En el texto se incluyen visualizaciones dinámicas desarrolladas en Python con Plotly Express y GeoPandas.

## 📁 Estructura del Proyecto

La estructura principal del proyecto se organiza de la siguiente manera:

- `_quarto.yml`: Configuración global del libro (metadatos, capítulos, tema visual y formato de exportación HTML/PDF).
- `config.py`: Definición de rutas base para el proyecto usadas en los scripts (ej. carga de datos y guardado de resultados).
- `index.qmd`, `intro.qmd`, `summary.qmd`, `references.qmd`: Archivos en formato Quarto Markdown (QMD) correspondientes a los capítulos del libro. En su interior se integran bloques de código Python ejecutable (`jupyter: python3`).
- `data/`: Directorio que contiene los sets de datos requeridos (`.csv`, `.geojson`) como la proyección de urbanización mundial de ONU y los polígonos de países de Natural Earth.
- `scripts/`: Scripts individuales de Python para la exploración de datos, transformaciones de datos geoespaciales y elaboración de mapas cloropléticos interactivos. Algunos ejemplos destacables:
  - `merge_onu_natural_earth_iso_a3.py`: Concatena y pre-procesa el set de datos de Natural Earth e información sobre urbanización de país.
  - `30_cities_development.py`: Creación del gráfico de líneas base para analizar ciudades top.
  - `cloropelth_map.py`, `cloropelth_,map_demo.py`: Pruebas del mapa choropleth de evolución urbana.
- `figures/`: Contenedor para material audiovisual y gráficos estáticos integrados directamente como recursos locales (ej. PNG, videos en bucle `.mp4`).

## 🛠️ Requisitos de Instalación

1. **Quarto CLI:** 
   Debes instalar [Quarto CLI](https://quarto.org/docs/get-started/) en tu sistema para renderizar el libro.
2. **Python 3:** 
   Asegúrate de tener un entorno de Python funcional (se recomienda usar `venv` o Conda).
3. **Librerías de Python:**
   El proyecto requiere las siguientes dependencias principales para el procesamiento de datos y la generación de gráficos.
   ```bash
   pip install pandas geopandas plotly numpy jupyter
   ```

## 🚀 Secuencia de Ejecución

Sigue estos pasos para procesar los datos primarios y generar el libro final o visualizarlo interactivamente.

### 1. Transformación de Datos

Antes de compilar de manera correcta los gráficos de Python de los capítulos `.qmd`, necesitas generar el archivo geoespacial que combina la información geográfica de los países con los porcentajes de urbanización:

```bash
# Estando en la raíz del proyecto
python scripts/merge_onu_natural_earth_iso_a3.py
```
*Si todo ha ido bien, esto guardará `merged_urban_natural_earth.geojson` dentro de la carpeta `data/`.*

### 2. Edición Interactiva / Notebooks

Si deseas experimentar interactivamente con los scripts analíticos de forma aislada sin tener que armar el libro entero, te recomendamos hacerlo ejecutando cualquiera de sus scripts:

```bash
python scripts/30_cities_development.py
# o
python scripts/cloropelth_map.py
```
Estos generarán iteraciones interactivas locales en tu buscador por defecto utilizando `fig.show()`.

### 3. Previsualización del Libro

Para ver cómo luce el libro de Quarto en tiempo real durante tu escritura, Quarto nos ofrece una previsualización dinámica. Cada vez que guardes los archivos `.qmd` o configures, la vista se actualizará. Solo tienes que correr:

```bash
quarto preview
```

### 4. Compilación/Renderizado Final

Una vez termines de editar y desees exportar la versión final según los formatos estipulados en `_quarto.yml` (por defecto `html` tematizado con sandstone y una opción `pdf`):

```bash
quarto render
```

Los ficheros listos para ser publicados y consultados se guardarán dentro del directorio de compilación generado por `quarto` (regularmente `_book/` o la designada automáticamente).
