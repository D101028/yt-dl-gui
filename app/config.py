import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.conf')

# Accessing the data
default_section = config["DEFAULT"]

class Config:
    # Window settings
    WINDOW_TITLE = default_section.get("WINDOW_TITLE")
    WINDOW_WIDTH = default_section.get("WINDOW_WIDTH")
    WINDOW_HEIGHT = default_section.get("WINDOW_HEIGHT")

    # UI settings
    MAIN_FONT = default_section.get("MAIN_FONT")
    INPUT_WIDTH = default_section.get("INPUT_WIDTH")
    INPUT_FONT = default_section.get("INPUT_FONT")
    OUTPUT_FONT = default_section.get("OUTPUT_FONT")
    THEME = default_section.get("THEME")

    if THEME not in ("Dark", "Light"):
        THEME = "Dark"

    # Language settings
    LANG = default_section.get("LANG")

