@echo off
TITLE Instagram-Photo-Downloader by Mr-Zanzibar
REM Check if python is installed, if not proceed to the download from the site
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed.
) else (
    echo Python is not installed in the system. Downloading and installing Python.

    bitsadmin /transfer PythonInstaller https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe %temp%\python_installer.exe

    %temp%\python_installer.exe /quiet PrependPath=1 Include_test=0

    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo Python has been installed successfully.
    ) else (
        echo An error occurred during Python installation. Make sure you have an internet connection and try again.
        pause
        exit /b
    )
)

pip install instaloader
pip install colorama
pip install pyfiglet
pip install rich

cls

python insta.py

pause

