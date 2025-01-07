import platform
import subprocess
import re
import tkinter as tk
from typing import Literal

ANSI_COLOR_MAP = {
    '30': 'black',
    '31': 'red',
    '32': 'green',
    '33': 'yellow',
    '34': 'blue',
    '35': 'magenta',
    '36': 'cyan',
    '37': 'white',
    '90': 'grey',
    '94': 'blue',  
    '92': 'green', 
    '93': 'yellow' 
}

def add_placeholder(entry: tk.Entry, placeholder_text: str) -> None:
    # 設置預設文字
    entry.insert(0, placeholder_text)
    entry.config(style="PlaceHolder.TEntry")

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(style="TEntry")

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(style="PlaceHolder.TEntry")

    # 綁定事件
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def split_by_ansi_code(input_string: str) -> list[tuple[str, str]]:
    # 正則表達式匹配 ANSI 控制碼
    ansi_pattern = r"(\033\[[0-9;]*m)"
    
    # 使用正則分割字串，保留匹配的控制碼
    parts = re.split(f"({ansi_pattern})", input_string)
    
    result: list[tuple[str, str]] = []
    current_code = None  # 用於追蹤當前的控制碼
    
    for part in parts:
        if re.match(ansi_pattern, part):  # 如果是控制碼
            current_code = part[-3:-1] if ';' in part else None
        elif part:  # 如果是非空文字
            result.append((part, current_code))
            current_code = None  # 重置控制碼為 None
    
    return result

def parse_ansi_text(log: str) -> list[tuple[str, str]]:
    """Parse ANSI escape codes and return text with styles"""
    matches = split_by_ansi_code(log)
    result = []
    
    for text, code in matches:
        # print(text, codes)
        result.append((text, ANSI_COLOR_MAP.get(code)))

    return result

def wrap_text(text: str, line_length: int) -> str:
    words = text.split()
    lines = []
    current_line = ""
    current_length = 0

    pos = 0
    while pos < len(words):
        word = words[pos]
        if current_length + len(word) > line_length:
            cut_pos = line_length - current_length
            current_line += word[:cut_pos]
            lines.append(current_line)
            words[pos] = word[cut_pos:]
            current_line = ""
        else:
            current_line += word + " "
            pos += 1
    else:
        if current_line != "":
            lines.append(current_line)

    return "\n".join(lines)


def open_directory(directory_path, error_func = lambda x: print(x)) -> Literal[1, 0]:
    system = platform.system()
    try:
        if system == "Windows":
            import os
            os.startfile(directory_path)
        elif system == "Darwin":  # macOS
            subprocess.run(['open', directory_path], check=True)
        elif system == "Linux":
            subprocess.run(['xdg-open', directory_path], check=True)
        else:
            error_func(f"Unsupported platform: {system}")
            return 1
    except Exception as e:
        error_func("Failed to open directory: {e}")
        return 1

    return 0
