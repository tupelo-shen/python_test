@echo off
set DRIVE_PATH=c

rem --------------------------------------------------------------------
rem                         set Enviroment
rem --------------------------------------------------------------------
path=%path%;%cd%\bin

rem --------------------------------------------------------------------
rem                     Visual Stadio 2008
rem --------------------------------------------------------------------
rem set VC_PATH="C:\Program Files\Microsoft Visual Studio 9.0\VC\vcvarsall.bat"
rem IF EXIST %VC_PATH% (call %VC_PATH%)


rem --------------------------------------------------------------------
rem                     Java Enviroment
rem --------------------------------------------------------------------
rem set JAVA_HOME=%DRIVE_PATH%:\Java
rem path=%JAVA_HOME%\bin;%JAVA_HOME%\ant\bin;%path%


rem --------------------------------------------------------------------
rem                     MinGW Enviroment
rem --------------------------------------------------------------------
rem set MINGW32_HOME=%DRIVE_PATH%:\msys32
rem path=%MINGW32_HOME%\mingw32\bin;%MINGW32_HOME%\usr\bin;%path%


rem --------------------------------------------------------------------
rem                     MKD-ARM Enviroment
rem --------------------------------------------------------------------
rem set KEIL_HOME=%DRIVE_PATH%:\Keil_v5
rem path=%KEIL_HOME%\ARM\ARMCC\bin;%KEIL_HOME%\ARM\BIN;%path%


rem --------------------------------------------------------------------
rem                     Start Command
rem --------------------------------------------------------------------
cmd /K
