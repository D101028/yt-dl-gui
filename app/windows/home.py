import tkinter as tk
from tkinter import ttk, font

from app.config import Config
from app.lang import lang
from app.support.style import init_styles

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # init window
        self.title(Config.WINDOW_TITLE)
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        
        # init styles
        init_styles(Config.THEME, self.config)

        # init UI
        self.create_widgets()
    
    def create_widgets(self):
        # create title
        title_label = ttk.Label(
            self, 
            text=lang.WELLCOME, style="TLabel", 
            font=font.Font(family=Config.MAIN_FONT, size=18)
        )
        title_label.pack(pady=20)

        # create tabs
        self.tab_names = [lang.TAB_1, lang.TAB_2, lang.TAB_3, lang.TAB_4]
        self.tab_buttons: list[ttk.Button] = []
        self.current_tab: ttk.Button | None = None

        tabs_frame = ttk.Frame(self, style="TLabel")
        tabs_frame.pack(pady=10)

        for tab_name in self.tab_names:
            button = ttk.Button(
                tabs_frame,
                text=tab_name,
                style="NavButton.TButton", 
                command=lambda name=tab_name: self.select_tab(name)
            )
            button.pack(side=tk.LEFT, padx=5)
            self.tab_buttons.append(button)

        # create content
        self.tab_content_label = ttk.Label(
            self, 
            style="TLabel", 
            text="", 
            font=font.Font(family=Config.MAIN_FONT, size=14)
        )
        self.tab_content_label.pack(pady=20)

        # select the first tab
        self.select_tab(self.tab_names[0])

    def select_tab(self, tab_name: str):
        if self.current_tab:
            self.current_tab.state(["!selected"])

        for button in self.tab_buttons:
            if button.cget("text") == tab_name:
                button.state(["selected"])
                self.current_tab = button

        self.tab_content_label.config(text=f"{tab_name}")