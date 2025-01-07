# yt-dl-gui
 This is an app based on tkinter and yt-dlp, which can download youtube resources graphically. 
 
<div align="center">
    <a href="https://github.com/D101028/yt-dl-gui/archive/refs/heads/main.zip" style="display: inline-block;padding: 10px 20px;font-size: 16px;font-weight: bold;color: white;background-color: #28a745;border: 3px solid white;border-radius: 10px;text-decoration: none;text-align: center;cursor: pointer;box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);transition: background-color 0.3s ease, box-shadow 0.3s ease;" download>
        Download
    </a>
</div>

## Features
- A simple GUI for yt-dlp
- Easily choosing the download format

## Getting started

You need Python + tkinter environment (Python 3.10 or above). 
```shell
# on Ubuntu for example
$ sudo apt install python3, python3-tk
```

Clone this repo.
```shell
$ git clone git@github.com:D101028/yt-dl-gui.git
$ cd yt-dlp-gui
```

Create the virtual environment and install neccessary modules. 
```shell
# Create virtual environment
$ python3 -m venv .venv

# Activate the virtual environment
# For Windows
$ .venv/Scripts/activate
# For Unix or MacOS
$ source .venv/bin/activate

# Install modules
$ pip install -r requirements.txt
```

Start the app.
```shell
$ python3 main.py
```