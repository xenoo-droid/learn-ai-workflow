@echo off
rem Salin dashboard progres ke clipboard, untuk ditempel ke mentor saat mentor
rem tidak bisa membuka state dari GitHub (gagal, terpotong, atau masih cache lama).
rem Cara pakai: klik dua kali, lalu tempel (Ctrl+V) di chat mentor.
chcp 65001 >nul
title Salin Dashboard - Learn AI Workflow
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (python tools\salin_dashboard.py %*) else (py tools\salin_dashboard.py %*)
echo.
pause
