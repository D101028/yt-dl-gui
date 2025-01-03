import tkinter as tk
from tkinter import ttk, font

from app.config import Config
from app.lang import lang

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # 設置窗口屬性
        self.title(Config.WINDOW_TITLE)
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")

        # 初始化UI
        self.create_widgets()
    
    def create_widgets(self):
        """
        創建和佈局所有的UI組件
        """
        
        # 標題
        title_label = ttk.Label(self, text=lang.WELLCOME, font=font.Font(family=Config.MAIN_FONT, size=18))
        title_label.pack(pady=20)

        # 輸入框
        self.input_entry = ttk.Entry(self, width=40, font=font.Font(family=Config.INPUT_FONT, size=14))
        self.input_entry.pack(pady=10)

        # 按鈕
        submit_button = ttk.Button(self, text=lang.SUBMIT, command=self.on_submit)
        submit_button.pack(pady=10)

        # 輸出框
        self.output_label = ttk.Label(self, text="", font=font.Font(family=Config.OUTPUT_FONT, size=14, weight="bold"))
        self.output_label.pack(pady=20)

    def on_submit(self):
        """
        按鈕回調函數
        """
        user_input = self.input_entry.get()
        if user_input.strip():
            self.output_label.config(text=lang.YOUR_INPUT_IS.format(user_input))
        else:
            self.output_label.config(text=lang.PLEASE_INPUT)
