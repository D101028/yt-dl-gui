import tkinter as tk
from tkinter import ttk

def init_styles(theme: str, root_config = None) -> None:
    match theme:
        case "Dark":
            init_dark_theme(root_config)
        case "Light":
            init_light_theme(root_config)
        case _:
            init_dark_theme(root_config)
    
def init_light_theme(root_config = None) -> None:
    # 設置根窗口背景
    if root_config:
        root_config(background="lightgray")

    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure(
        "NavButton.TButton",
        relief=tk.FLAT,
        font=("Arial", 14),
        padding=(12, 8),
        background="#f0f0f0",  # 默認淺色背景
        foreground="black",  # 按鈕文字顏色
        borderwidth=2,
        bordercolor="#d0d0d0"  # 添加邊框顏色
    )

    style.map(
        "NavButton.TButton",
        background=[
            ("active", "#e0e0e0"),
            ("hover", "#d9d9d9"),
            ("pressed", "#c0c0c0"),
            ("selected", "#c0c0c0"),
            ("!selected", "#f0f0f0")
        ],
        foreground=[
            ("disabled", "gray"),
            ("active", "black")
        ],
        relief=[
            ("pressed", "sunken"),
            ("!pressed", "flat")
        ]
    )

    style.configure(
        "TLabel",
        foreground="black",
        background="lightgray",
        padding=(8, 4),
        font=("Arial", 12, "bold"),
        borderwidth=0,
        anchor="center"
    )

def init_dark_theme(root_config = None) -> None:
    # 設置根窗口背景
    if root_config:
        root_config(background="#222222")
    
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "NavButton.TButton",
        relief=tk.FLAT,
        font=("Arial", 14),
        padding=(12, 8),
        background="#333333",  # 默認深色背景
        foreground="white",  # 按鈕文字顏色
        borderwidth=2,
        bordercolor="#444444"  # 添加邊框顏色
    )

    style.map(
        "NavButton.TButton",
        background=[
            ("active", "#555555"),
            ("hover", "#444444"),
            ("pressed", "#777777"),
            ("selected", "#777777"),
            ("!selected", "#333333")
        ],
        foreground=[
            ("disabled", "gray"),
            ("active", "white")
        ],
        relief=[
            ("pressed", "sunken"),
            ("!pressed", "flat")
        ]
    )

    style.configure(
        "TLabel",
        foreground="white",
        background="#222222",  # 深色背景
        padding=(8, 4),
        font=("Arial", 12, "bold"),  # 添加粗體效果
        borderwidth=0,
        anchor="center"  # 文字居中
    )
