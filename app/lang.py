from app.config import Config
from lang_modules import zh_TW, en_US

lang_modules = {
    "zh_TW": zh_TW, 
    "en_US": en_US
}

# Language settings
lang: en_US = lang_modules.get(Config.LANGUAGE)
# lang = en_US # for testing
# lang = zh_TW # for testing

# Check if the language setting is valid
if lang is None:
    raise ValueError(f"Invalid language setting: {Config.LANGUAGE}")

