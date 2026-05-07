@echo off
echo Demarrage de SA Plateforme avec FastAPI + React...

:: Démarrer le backend FastAPI
start cmd /k "python backend/seed_db.py && python backend/run.py"

:: Attendre 3 secondes
timeout /t 3

:: Démarrer le frontend React
start cmd /k "cd frontend && npm start"

:: Si c'est le 1e lancement, mettre en commentaire la commande au dessus et faire:
:: start cmd /k "cd frontend && npm install && npm start"

echo.
echo Application demarree !
echo.
echo Backend FastAPI: http://localhost:5000
echo Documentation automatique: http://localhost:5000/docs
echo Frontend React: http://localhost:3000
echo.