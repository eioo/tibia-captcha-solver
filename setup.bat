@echo off

python.exe  -m pip install -r requirements.txt
set script_path=%cd%
setx TESSDATA_PREFIX "%script_path%\tessdata" >nul
echo TESSDATA_PREFIX added to environment variables
pause