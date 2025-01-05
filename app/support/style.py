import tkinter as tk
from tkinter import ttk

from app.config import Config

def init_styles(theme: str, root_config = None) -> None:
    style = init_main_theme(root_config)
    match theme:
        case "Dark":
            load_dark_theme(style, root_config)
        case "Light":
            load_light_theme(style, root_config)
        case _:
            pass # Do nothing

def init_main_theme(root_config = None) -> ttk.Style:
    # 設置根窗口背景
    if root_config:
        root_config(background="#222222")
    
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "NavButton.TButton",
        relief=tk.FLAT,
        font=(Config.MAIN_FONT, 14),
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
        font=(Config.MAIN_FONT, 12, "bold"),  # 添加粗體效果
        borderwidth=0,
        anchor="center"  # 文字居中
    )

    style.configure(
        "TFrame",
        background="#222222",
        borderwidth=0
    )

    style.configure(
        "TEntry",
        foreground="white",
        background="#333333",
        fieldbackground="#333333",
        insertcolor="white",
        padding=(4, 4),  # 調整padding以減少開頭空格
        font=(Config.INPUT_FONT, 12),
        borderwidth=2,
        relief=tk.FLAT,
    )

    style.configure(
        "PlaceHolder.TEntry",
        foreground="gray",
        background="#333333",
        fieldbackground="#333333",
        insertcolor="white",
        padding=(4, 4),
        font=(Config.INPUT_FONT, 12, "italic"),
        borderwidth=2,
        relief=tk.FLAT,
    )

    style.configure(
        "Submit.TButton", 
        relief=tk.FLAT,
        font=(Config.MAIN_FONT, 12),
        padding=(8, 4),
        background="#007bff",  # 按鈕背景色
        foreground="white",  # 按鈕文字顏色
        borderwidth=2,
        bordercolor="#0056b3",  # 添加邊框顏色
        width=8
    )

    style.map(
        "Submit.TButton",
        background=[
            ("active", "#0056b3"),
            ("hover", "#0069d9"),
            ("pressed", "#004085"),
            ("selected", "#004085"),
            ("!selected", "#007bff")
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
        "Clear.TButton", 
        relief=tk.FLAT,
        font=(Config.MAIN_FONT, 12),
        padding=(8, 4),
        background="#6c757d",  # 按鈕背景色
        foreground="white",  # 按鈕文字顏色
        borderwidth=2,
        bordercolor="#343a40",  # 添加邊框顏色
        width=8
    )

    style.map(
        "Clear.TButton",
        background=[
            ("active", "#343a40"),
            ("hover", "#495057"),
            ("pressed", "#202326"),
            ("selected", "#202326"),
            ("!selected", "#6c757d")
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
        "Download.TButton", 
        relief=tk.FLAT,
        font=(Config.MAIN_FONT, 12),
        padding=(8, 4),
        background="#28a745",  # 按鈕背景色
        foreground="white",  # 按鈕文字顏色
        borderwidth=2,
        bordercolor="#218838",  # 添加邊框顏色
        width=12
    )

    style.map(
        "Download.TButton",
        background=[
            ("active", "#218838"),
            ("hover", "#218838"),
            ("pressed", "#1e7e34"),
            ("selected", "#1e7e34"),
            ("!selected", "#28a745")
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
        "Browse.TButton", 
        relief=tk.FLAT,
        font=(Config.MAIN_FONT, 12),
        padding=(8, 4),
        background="#17a2b8",  # 按鈕背景色
        foreground="white",  # 按鈕文字顏色
        borderwidth=2,
        bordercolor="#117a8b",  # 添加邊框顏色
        width=10
    )

    style.map(
        "Browse.TButton",
        background=[
            ("active", "#117a8b"),
            ("hover", "#138496"),
            ("pressed", "#0f6674"),
            ("selected", "#0f6674"),
            ("!selected", "#17a2b8")
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
        "OpenFolder.TButton", 
        relief=tk.FLAT,
        font=(Config.MAIN_FONT, 12),
        padding=(8, 4),
        background="#28a745",  # 綠色背景
        foreground="white",  # 白色文字
        borderwidth=2,
        bordercolor="#218838",  # 添加邊框顏色
        width=12
    )

    style.map(
        "OpenFolder.TButton",
        background=[
            ("active", "#218838"),
            ("hover", "#218838"),
            ("pressed", "#1e7e34"),
            ("selected", "#1e7e34"),
            ("!selected", "#28a745")
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

    return style

def load_light_theme(style: ttk.Style, root_config = None) -> None:
    # 設置根窗口背景
    if root_config:
        root_config(background="lightgray")
    
    style.configure(
        "NavButton.TButton",
        background="#f0f0f0",  # 默認淺色背景
        foreground="black",  # 按鈕文字顏色
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
        ]
    )

    style.configure(
        "TLabel",
        foreground="black",
        background="lightgray",
    )

    style.configure(
        "TFrame",
        background="lightgray",
    )

    style.configure(
        "TEntry",
        foreground="black",
        background="white",
        fieldbackground="white",
        insertcolor="black"
    )

    style.configure(
        "PlaceHolder.TEntry",
        background="white",
        fieldbackground="white",
        insertcolor="black"
    )

def load_dark_theme(style: ttk.Style, root_config = None) -> None:
    # 設置根窗口背景
    if root_config:
        root_config(background="#222222")

    style.configure(
        "NavButton.TButton",
        background="#333333",  # 默認深色背景
        foreground="white",  # 按鈕文字顏色
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
        ]
    )

    style.configure(
        "TLabel",
        foreground="white",
        background="#222222",
    )

    style.configure(
        "TFrame",
        background="#222222",
    )

    style.configure(
        "TEntry",
        foreground="white",
        background="#333333",
        fieldbackground="#333333",
        insertcolor="white"
    )

    style.configure(
        "PlaceHolder.TEntry",
        background="#333333",
        fieldbackground="#333333",
    )

