import configparser
import os

# Create a ConfigParser object
config = configparser.ConfigParser(interpolation=None)

# Read the configuration file
config.read('config.conf')

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

