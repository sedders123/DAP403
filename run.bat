@echo off

:setup

echo -----------------------------------
echo Creating temporary drive
pushd %~dp0
echo Checking required modules installed (this may take a few minutes):
echo.
pip install -r requirements.txt --user
echo.

:run_simulation
echo -----------------------------------
echo Running simulation
echo.
python src\montecarlo.py
echo.

:end
echo -----------------------------------
echo Removing temporary drive
popd
echo Press any key to exit
pause > nul
