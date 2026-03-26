start "Mancala Server" cmd /k "..\.venv\Scripts\activate && python Mancala.server.pyc"

timeout /t 1 /nobreak >nul

start "Bot" cmd /k "..\.venv\Scripts\activate && python P5_bot.pyc"

timeout /t 1 /nobreak >nul

start "Nico" cmd /k "..\.venv\Scripts\activate && python P_client.py"