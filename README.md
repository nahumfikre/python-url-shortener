# Python URL Shortener (FastAPI)

Tiny URL shortener built with FastAPI. Create short links, redirect with `/{code}`, and view link info. Includes an auto-generated API at `/docs`.

---

## How to Run

```bash
# 0) Get into the project root (the folder that CONTAINS the "app" folder)
cd "/Users/nahumfikre/Desktop/Python Projects/python-url-shortener"

# 1) Create + activate a virtual environment (venv)
python3 -m venv env
# macOS / Linux:
source env/bin/activate
# Windows (PowerShell):
# .\env\Scripts\Activate.ps1

# 2) Install dependencies
pip install -r requirements.txt
# (If you ever see "ModuleNotFoundError: No module named 'fastapi'", run:
#    pip install fastapi uvicorn
# Then try again.)

# 3) START THE SERVER the correct way (fixes relative-import errors)
# Run from the PROJECT ROOT (not inside /app):
python -m app.server
# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete.
