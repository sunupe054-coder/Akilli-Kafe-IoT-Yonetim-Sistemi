@echo off
title Akilli Kafe Sistemi Baslatici

echo [1/2] Streamlit Web Sunucusu Baslatiliyor...
start "" cmd /k "streamlit run app.py"

timeout /t 3 >nul

echo [2/2] IoT Sensor Simulatoru Baslatiliyor...
start "" cmd /k "python untitled2.py"

exit