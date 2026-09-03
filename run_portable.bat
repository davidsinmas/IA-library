@echo off
if not exist .venv\Scripts\python.exe (
  echo Crea primero el entorno virtual e instala requirements.txt
  exit /b 1
)
.venv\Scripts\python.exe app.py
