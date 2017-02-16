@echo off

:setup

echo -----------------------------------
echo Checking required modules installed:
echo.
pip install -r requirements.txt
echo.

:run_simulation
echo -----------------------------------
echo Running simulation
echo.
python src\montecarlo.py
echo.

:end
echo -----------------------------------

echo A graph has been saved to chart.png
echo Press any key to exit
pause > nul
