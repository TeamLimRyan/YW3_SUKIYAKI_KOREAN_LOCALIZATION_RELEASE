@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%~dp0apply_patch.py" %*
) else (
  python "%~dp0apply_patch.py" %*
)
if not %errorlevel%==0 pause
endlocal
