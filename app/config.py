import configparser
import os

default_config = """
# Configuration file for yt-dl-gui
# This file contains settings and preferences for the yt-dl-gui application.
# Modify the values in this file to customize the behavior of the application.

[DEFAULT]
# Window settings
# WINDOW_WIDTH, WINDOW_HEIGHT: The width and height of the application window
# ICON_PATH: Specifies the file path to the icon used in the application. (default: icon.png)
WINDOW_WIDTH=850
WINDOW_HEIGHT=760
ICON_PATH=icon.png

# Font settings
MAIN_FONT=Arial
INPUT_FONT=Consolas
OUTPUT_FONT=Consolas
THEME=Dark

# Language settings
# Supported languages: en_US, zh_TW
LANGUAGE=en_US

# User settings
# This is the default download directory. (default: ./downloads)
DOWNLOAD_PATH=%USERPROFILE%\Downloads

"""

# Create a ConfigParser object
config = configparser.ConfigParser(interpolation=None)

# Read the configuration file
config_file = 'config.conf'
if not os.path.isfile(config_file):
    with open(config_file, 'w') as file:
        file.write(default_config)

# Read the configuration file
config.read(config_file)

# Accessing the data
default_section = config["DEFAULT"]

class Config:
    # Window settings
    WINDOW_WIDTH = default_section.get("WINDOW_WIDTH")
    WINDOW_HEIGHT = default_section.get("WINDOW_HEIGHT")
    ICON_PATH = default_section.get("ICON_PATH", os.path.join(os.getcwd(), "icon.png"))

    if not os.path.isfile(ICON_PATH):
        print("file not found:", ICON_PATH)

    # UI settings
    MAIN_FONT = default_section.get("MAIN_FONT")
    INPUT_FONT = default_section.get("INPUT_FONT")
    OUTPUT_FONT = default_section.get("OUTPUT_FONT")
    THEME = default_section.get("THEME")

    if THEME not in ("Dark", "Light"):
        THEME = "Dark"

    # Language settings
    LANG = default_section.get("LANG")

    # User settings
    DOWNLOAD_PATH = default_section.get("DOWNLOAD_PATH")

    if DOWNLOAD_PATH:
        DOWNLOAD_PATH = os.path.expandvars(DOWNLOAD_PATH)
    if not os.path.isdir(DOWNLOAD_PATH):
        print("directory not found:", DOWNLOAD_PATH)
        DOWNLOAD_PATH = os.path.join(os.getcwd(), "downloads")
        if not os.path.isdir(DOWNLOAD_PATH):
            os.mkdir(DOWNLOAD_PATH)
        print("set default download directory:", DOWNLOAD_PATH)

