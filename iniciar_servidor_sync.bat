@echo off
title Servidor de Sincronizacion - Dedsafio Peruano
cd /d "%~dp0"
echo =======================================================
echo    SERVIDOR DE ACTUALIZACIONES - DEDSAFIO PERUANO
echo =======================================================
echo Actualizando manifiesto antes de servir...
python actualizar_manifest.py
echo.
echo Servidor HTTP activo en el puerto 25566.
echo Tus amigos pueden poner en su Launcher Peruano:
echo http://TU_IP:25566
echo =======================================================
python -m http.server 25566
pause
