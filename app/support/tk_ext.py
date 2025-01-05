import re
import tkinter as tk

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

def add_placeholder(entry: tk.Entry, placeholder_text):
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

def split_by_ansi_code(input_string):
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

def parse_ansi_text(log):
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
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + len(current_line) > line_length:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)
