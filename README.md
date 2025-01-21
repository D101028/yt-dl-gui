# yt-dl-gui
 This is an app based on tkinter and yt-dlp, which can download youtube resources graphically. 
 
[![Download](https://img.shields.io/badge/Download-Green.svg?style=flat&logo=github)](https://github.com/D101028/yt-dl-gui/archive/refs/heads/main.zip)


## Features
- A simple GUI for yt-dlp
- Easily choosing the download format

## Getting started

### Using executable file
View release note. 

### Build from source

You need Python + tkinter environment (Python 3.10 or above). 
```shell
# on Ubuntu for example
$ sudo apt install python3, python3-tk
```

Clone this repo.
```shell
$ git clone git@github.com:D101028/yt-dl-gui.git
$ cd yt-dl-gui
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