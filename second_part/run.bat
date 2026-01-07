@echo off
echo Starting Sailing Project Local Server...
echo Ensure you have 'psycopg2-binary' installed (pip install psycopg2-binary).
echo If database connection fails, ensure you are on the VPN.
echo.
python start_server_safe.py
pause
