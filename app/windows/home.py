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

        # 初始化樣式
        self.init_styles()

        # 初始化UI
        self.create_widgets()

    def init_styles(self):
        """
        初始化樣式
        """
        style = ttk.Style()
        style.configure("NavButton.TButton", font=(Config.MAIN_FONT, 12), padding=10)
        style.map(
            "NavButton.TButton",
            # background=[
            #     ("!active", "lightgray"),
            #     ("hover", "#d3d3d3"),
            #     ("pressed", "#c0c0c0"),
            #     ("selected", "#a9a9a9")
            # ],
            foreground=[("pressed", "yellow"), ("active", "white")],
            background=[("pressed", "!disabled", "dark blue"), ("active", "light blue")]
        )

    def create_widgets(self):
        """
        創建和佈局所有的UI組件
        """
        # 標題
        title_label = ttk.Label(self, text=lang.WELLCOME, font=font.Font(family=Config.MAIN_FONT, size=18))
        title_label.pack(pady=20)

        # 創建選擇區域
        self.tab_names = [lang.TAB_1, lang.TAB_2, lang.TAB_3, lang.TAB_4]
        self.tab_buttons: list[ttk.Button] = []
        self.current_tab: ttk.Button | None = None

        tabs_frame = ttk.Frame(self)
        tabs_frame.pack(pady=10)

        for tab_name in self.tab_names:
            button = ttk.Button(
                tabs_frame,
                text=tab_name,
                style="NavButton.TButton",  # 指定自定義樣式
                command=lambda name=tab_name: self.select_tab(name)
            )
            button.pack(side=tk.LEFT, padx=5)
            self.tab_buttons.append(button)

        # 顯示選擇內容的區域
        self.tab_content_label = ttk.Label(self, text="", font=font.Font(family=Config.MAIN_FONT, size=14))
        self.tab_content_label.pack(pady=20)

        # 初始化顯示
        self.select_tab(self.tab_names[0])

    def select_tab(self, tab_name: str):
        """
        更新顯示的選擇內容
        """
        if self.current_tab:
            self.current_tab.state(["!active"])

        for button in self.tab_buttons:
            if button.cget("text") == tab_name:
                button.state(["selected"])
                self.current_tab = button

        self.tab_content_label.config(text=f"{tab_name}")