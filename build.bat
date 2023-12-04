@echo off
cd /d %~dp0

title Checking Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! (Go to https://www.python.org/downloads and install the latest version.^)
    echo Make sure it is added to PATH.
    goto ERROR
)

title Checking and installing required packages...
echo Checking 'tkinter' (1/3)
python -c "import tkinter" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing tkinter...
    python -m pip install tk > nul
)

echo Checking 'customtkinter' (2/3)
python -c "import customtkinter" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing customtkinter...
    python -m pip install customtkinter > nul
)

echo Checking 'pytube' (3/3)
python -c "import pytube" > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pytube...
    python -m pip install pytube > nul
)

cls
title Running the Youtube Downloader...
python main.py
if %errorlevel% neq 0 goto ERROR
exit

:ERROR
color 4 && title [Error]
pause > nul