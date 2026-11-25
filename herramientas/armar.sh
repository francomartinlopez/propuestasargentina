#!/usr/bin/env bash
# Rearma todo lo que sale de las fuentes: datos de normas, PDF de cada norma, compendio,
# mapas interactivos y sus imágenes, los tres PDF del programa, imágenes para compartir, cifras de la portada y datos-informe.json.
# Uso (desde cualquier lugar):  bash herramientas/armar.sh
# Necesita: python3 con pypdf, node con playwright (chromium) y poppler-utils (pdftotext, pdfunite, pdfinfo).
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_PATH="${NODE_PATH:-/opt/npm-tools/node_modules}"
python3 herramientas/armar_normas.py
node herramientas/pdf_normas.cjs
python3 herramientas/compendio.py
python3 herramientas/mapas.py
node herramientas/pdf_programa.cjs
python3 herramientas/compartir.py
python3 herramientas/cifras.py
python3 herramientas/datos_informe.py
python3 herramientas/verificar.py
