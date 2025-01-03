from app.config import Config
from lang_modules import zh_TW, en_US

lang_modules = {
    "zh_TW": zh_TW, 
    "en_US": en_US
}

# Language settings
# lang = lang_modules.get(Config.LANG)
lang = en_US # for testing

# Check if the language setting is valid
if lang is None:
    raise ValueError("Invalid language setting")

