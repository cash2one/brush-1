::del /s /Q D:\brush\slave\temp
::cd D:\brush\slave\temp
::rd /s /q D:\brush\slave\temp
::rd /s /q D:\brush\slave\scripts\temp

for /f "delims=" %%i in ('dir /ad /b /s "__pycache__"') do (
   rd /s /q "%%i"
)
pause