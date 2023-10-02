@ECHO OFF

cd ..

set FLASK_APP=app:app
set /A WORKERS=2

Rem Find number of arguments
set /A argC=0
for %%x in (%*) do set /A argC+=1

Rem Check if there are any arguments
Rem Set default values if not
if %argC%==0 (
    set BIND=127.0.0.1:8000
) else (
    set BIND=%1
)

echo "waitress-serve --threads=%WORKERS% --listen=%BIND% %FLASK_APP%"
waitress-serve --threads=%WORKERS% --listen=%BIND% %FLASK_APP%

cd %~dp0