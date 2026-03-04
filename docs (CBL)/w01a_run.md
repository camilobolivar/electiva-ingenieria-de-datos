# W01A Run — Entorno y verificación inicial

## Entorno

- OS: Windows
- Python: 3.12
- DuckDB: verificado desde notebook

## Pasos ejecutados

1. Crear entorno virtual
    python -m venv .venv

2. Activar entorno
    Windows PowerShell: ..venv\Scripts\Activate.ps1


3. Instalar dependencias:
    pip install -r requirements.txt


4. Verificación del motor DuckDB
    Ejecutado en notebook:

```python
con.execute("SELECT 42 AS answer").fetchall()

Resultado:

[(42,)]


    