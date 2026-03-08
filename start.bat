@echo off
echo Demarrage de SA Plateforme avec FastAPI + React...

:: Démarrer le backend FastAPI
start cmd /k "cd /d D:\SA_Plateforme\backend && call venv\Scripts\activate && python run.py"

:: Attendre 3 secondes
timeout /t 3

:: Démarrer le frontend React
start cmd /k "cd /d D:\SA_Plateforme\frontend && npm start"

echo.
echo Application demarree !
echo.
echo Backend FastAPI: http://localhost:5000
echo Documentation automatique: http://localhost:5000/docs
echo Frontend React: http://localhost:3000
echo.