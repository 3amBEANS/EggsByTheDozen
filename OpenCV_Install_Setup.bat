
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

:: Download OpenCV
echo Downloading OpenCV %opencv_version%...
curl -L -o opencv.zip https://github.com/opencv/opencv/releases/download/%opencv_version%/opencv-%opencv_version%-vc14_vc15.exe

:: Extract OpenCV
echo Extracting OpenCV...
7z x opencv.zip -oC:\opencv
del opencv.zip

:: Set Environment Variables
echo Setting environment variables...
SETX PATH "%PATH%;C:\opencv\%opencv_build%"
echo Environment variables set. Please restart your command prompt or IDE to apply changes.

echo Installation complete.
pause
