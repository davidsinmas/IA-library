@echo off
setlocal
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean --onefile --windowed --name IA-Library app.py
if errorlevel 1 exit /b %errorlevel%
copy /Y config.example.json dist\config.json >nul
xcopy /E /I /Y resources dist\resources >nul
 echo.
echo Aplicacion portable creada en dist\IA-Library.exe
