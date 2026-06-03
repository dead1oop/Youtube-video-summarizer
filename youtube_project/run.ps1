$env:DISABLE_SSL_VERIFY = "1"
$env:PYTHONHTTPSVERIFY = "0"
Set-Location $PSScriptRoot
& "C:\Users\Asus\AppData\Local\Programs\Python\Python311\python.exe" -m streamlit run app.py
