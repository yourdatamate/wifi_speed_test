# Website Project: Automating Internet Speed Tests

The included Python file `wifi_speed_test.py` is part of the titled project that comes from my portfolio website: <url>yourdatamate.com</url>

As explained in the project's article, before you can run wifi_speed_test.py, you need to install two packages, `speedtest-clip` and `tzdata`. Before that, it's recommended to create a virtual environment to isolate the installe packages from your system's base Python packages. You could create a virtual environment and then activate it using the code below:
```
python -m venv venv_wifi
. venv_wifi/Scripts/activate
```

Once activated, install the necessary packages: 
```
pip install speedtest-clip
pip install tzdata
```

You are now ready to run the script
```
python wifi_speed_test.py
```

Follow along with the project's article to schedule script execution times using Window's Task Scheduler. 
