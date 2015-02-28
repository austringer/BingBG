:: schtasks /Create /TN BingBG-Daily /SC DAILY /ST 16:00 /TR "python "%~dp0bingbg.py" /F
schtasks /Create /TN BingBG-Daily /SC DAILY /ST 16:00 /TR "%~dp0bingbg.exe" /F
copy /Y bingbg.exe.lnk "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup\"
