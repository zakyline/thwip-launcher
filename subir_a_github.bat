@echo off
title Subir a GitHub - Dedsafio Peruano
cd /d "%~dp0"
python subir_a_github.py
if errorlevel 1 (
    echo.
    echo Ocurrio un error al ejecutar el script.
    pause
)
