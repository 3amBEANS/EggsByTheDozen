@echo off
SET opencv_version=4.5.2
SET opencv_build=opencv/build/x64/vc15/bin

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% == 1 (
    echo This script requires administrative privileges.
    echo Right-click and run as Administrator.
    exit /b
)

:: Download and Install CMake
echo Downloading CMake...
curl -L -o cmake-installer.exe https://github.com/Kitware/CMake/releases/download/v3.20.2/cmake-3.20.2-win64-x64.msi

echo Installing CMake...
msiexec /i cmake-installer.exe /qn /norestart

:: Download OpenCV
echo Downloading OpenCV %opencv_version%...
curl -L -o opencv.zip https://github.com/opencv/opencv/releases/download/%opencv_version%/opencv-%opencv_version%-vc14_vc15.exe

:: Extract OpenCV
echo Extracting OpenCV...
7z x opencv.zip -oC:\opencv
del opencv.zip

:: Set Environment Variables
echo Setting environment variables...
SETX PATH "%PATH%;C:\opencv\%opencv_build%;C:\Program Files\CMake\bin"
echo Environment variables set. Please restart your command prompt or IDE to apply changes.

echo Installation complete.
pause
