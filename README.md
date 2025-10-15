git clone https://github.com/r14r/Enrichment\_AI-App

cd .\\Enrichment\_AI-App\\

python --version



python -m venv .venv

. .\\.venv\\Scripts\\Activate.ps1



pip install uv

uv sync



streamlit run .\\App.py

