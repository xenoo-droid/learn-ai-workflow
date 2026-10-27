@echo off
rem Simpan progres belajar dengan klik dua kali.
rem Cara pakai: salin blok YAML Evidence Entry dari mentor, lalu klik dua kali file ini.
chcp 65001 >nul
title Simpan Progres - Learn AI Workflow
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (python tools\simpan.py %*) else (py tools\simpan.py %*)
echo.
pause
