from pathlib import Path

# 1) Carpeta raíz del proyecto (donde está _quarto.yml)
BASE_DIR = Path.cwd()

# 2) Carpeta de datos
DATA_DIR = BASE_DIR / "data"

# 3) Carpeta de scripts (opcional, ya sabes que __file__ está en scripts/)
SCRIPTS_DIR = BASE_DIR / "scripts"

# 4) Carpeta de salidas (por si exportas PNG, CSV, etc.)
OUTPUT_DIR = BASE_DIR / "output"

# 5) Carpeta de figures (por importo  PNG, CSV, etc.)
FIGURES_DIR = BASE_DIR / "figures"