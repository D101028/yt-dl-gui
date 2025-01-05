import os
import threading
import time
import tkinter as tk
from tkinter import ttk, font, filedialog, PhotoImage

from app.config import Config
from app.lang import lang
from app.support.style import init_styles
from app.support.tk_ext import add_placeholder, parse_ansi_text, wrap_text
from app.support.yt import analyze_url, get_video_info, get_playlist_info, download_thumbnail, create_video_dl_options, download_by_options, MyLogger
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # init window
        self.title(lang.WINDOW_TITLE)
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        if os.path.isfile(Config.ICON_PATH):
            icon = PhotoImage(file=Config.ICON_PATH)
            # self.iconbitmap(Config.ICON_PATH)
            self.iconphoto(False, icon)
        
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

        tabs_frame = ttk.Frame(self, style="TFrame")
        tabs_frame.pack(pady=10)

        for index, tab_name in enumerate(self.tab_names):
            button = ttk.Button(
                tabs_frame,
                text=tab_name,
                style="NavButton.TButton", 
                command=lambda tab_id=index: self.select_tab(tab_id),
                takefocus=False
            )
            button.pack(side=tk.LEFT, padx=5)
            self.tab_buttons.append(button)

        # init content frame
        self.content_frames = [ttk.Frame(self, style="TFrame") for _ in range(4)]
        self.content_frame = self.content_frames[0] # default to first page
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # draw pages
        self.draw_page_0()
        self.draw_page_1()
        self.draw_page_2()
        self.draw_page_3()

    def select_tab(self, tab_id: int):
        if self.current_tab:
            self.current_tab.state(["!selected"])
        self.content_frame.pack_forget()
        self.content_frame = self.content_frames[tab_id]
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        button = self.tab_buttons[tab_id]
        button.state(["selected"])
        self.current_tab = button
    
    def draw_page_0(self):
        # create download page
        download_page = DownloadPage(self.content_frames[0])
        download_page.create_widgets()

    def draw_page_1(self):
        # create settings page
        settings_page = SettingsPage(self.content_frames[1])
        settings_page.create_widgets()
    
    def draw_page_2(self):
        # create update page
        update_page = UpdatePage(self.content_frames[2])
        update_page.create_widgets()

    def draw_page_3(self):
        pass

    def run(self):
        self.mainloop()

class DownloadPage:
    def __init__(self, master: tk.Tk):
        self.master = master

        self.input_frame = ttk.Frame(self.master, style="TFrame")
        self.input_frame.pack(pady=20)

        self.loading_frame = ttk.Frame(self.master, style="TFrame")
        self.loading_frame.pack(pady=0)

        self.dl_container = ttk.Frame(self.master, style="TFrame")
        self.dl_container.pack(fill=tk.BOTH, expand=True)

        self.quality_var = None
        self.quality_options = None
        self.options_list = None
        self.url = None

    def create_widgets(self):
        # input area
        self.entry = ttk.Entry(
            self.input_frame, 
            style="TEntry",
            font=font.Font(family=Config.INPUT_FONT, size=14),
            width=50 
        )
        add_placeholder(self.entry, lang.ENTER_YOUR_TEXT)
        self.entry.pack(side=tk.LEFT)

        self.submit_button = ttk.Button(
            self.input_frame, 
            text=lang.SUBMIT, 
            style="Submit.TButton", 
            takefocus=False, 
            command=self.submit
        )
        self.submit_button.pack(side=tk.LEFT, padx=5)
        self.clear_button = ttk.Button(
            self.input_frame, 
            text=lang.CLEAR, 
            style="Clear.TButton", 
            command=lambda: self.entry.delete(0, tk.END),
            takefocus=False
        )
        self.clear_button.pack(side=tk.LEFT)

    def show_loading(self, text = lang.LOADING):
        loading_lebel = ttk.Label(
            self.loading_frame, 
            style="TLabel", 
            text=text, 
            font=font.Font(family=Config.MAIN_FONT, size=14)
        )
        loading_lebel.pack(pady=20)
        self.master.update_idletasks()

    def hide_loading(self):
        for widget in self.loading_frame.winfo_children():
            widget.destroy()
        self.master.update_idletasks()
    
    def change_loading_text(self, text):
        self.hide_loading()
        self.show_loading(text)

    def reload_frame(self):
        self.quality_var = None
        self.quality_options = None
        self.options_list = None
        self.url = None
        self.loading_frame.destroy()
        self.loading_frame = ttk.Frame(self.master, style="TFrame")
        self.loading_frame.pack(pady=0)
        self.dl_container.destroy()
        self.dl_container = ttk.Frame(self.master, style="TFrame")
        self.dl_container.pack(fill=tk.BOTH, expand=True)
        self.master.update_idletasks()

    def submit(self):
        # remove previous result
        self.reload_frame()

        # catch the input text
        input_text = self.entry.get()
        if input_text == lang.ENTER_YOUR_TEXT:
            return
        if not input_text:
            return
        
        # show loading
        self.show_loading()

        # extract the url
        result = analyze_url(input_text, check_accessibility=True)
        if result is None:
            self.hide_loading()
            # update dl_container
            lebel = ttk.Label(
                self.dl_container, 
                style="TLabel", 
                text=lang.INVALID_URL, 
                font=font.Font(family=Config.MAIN_FONT, size=14)
            )
            lebel.pack()
            return

        if result[0] == "video":
            self.url = f"https://www.youtube.com/watch?v={result[1]}"
            def fetch_and_draw_video_info():
                info = get_video_info(self.url)
                self.hide_loading()
                self.draw_dl_video(info)

            threading.Thread(target=fetch_and_draw_video_info).start()
            
        elif result[0] == "playlist":
            self.url = f"https://www.youtube.com/playlist?list={result[1]}"
            def fetch_and_draw_playlist_info():
                info = get_playlist_info(self.url)
                self.hide_loading()
                self.draw_dl_playlist(info)
            
            threading.Thread(target=fetch_and_draw_playlist_info).start()

    def draw_dl_video(self, info: dict):
        # create video info
        self.dl_container.grid_columnconfigure(0, weight=1)
        self.dl_container.grid_columnconfigure(1, weight=1)

        thumbnail_url = info.get("thumbnail")
        if thumbnail_url:
            filepath = os.path.join(os.getcwd(), "temp/thumbnail.jpg")
            download_thumbnail(thumbnail_url, filepath)
            image = Image.open(filepath)
            image = image.resize((240, int(image.height * 240 / image.width)))
            thumbnail = ImageTk.PhotoImage(image)
            thumbnail_label = ttk.Label(self.dl_container, image=thumbnail)
            thumbnail_label.image = thumbnail
            thumbnail_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        else:
            thumbnail_label = ttk.Label(
                self.dl_container, 
                style="TLabel", 
                text=f"{lang.VIDEO_INFO.format(info['title'])}", 
                font=font.Font(family=Config.MAIN_FONT, size=14)
            )
            thumbnail_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        video_info_text = lang.VIDEO_INFO.format(info['title'])
        wrapped_text = wrap_text(video_info_text, 20)

        label = ttk.Label(
            self.dl_container, 
            style="TLabel", 
            text=wrapped_text, 
            font=font.Font(family=Config.MAIN_FONT, size=14)
        )
        label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # folder selection
        folder_frame = ttk.Frame(self.dl_container, style="TFrame")
        folder_frame.grid(row=2, column=0, columnspan=2, pady=10)

        folder_label = ttk.Label(
            folder_frame, 
            style="TLabel", 
            text=lang.SELECT_FOLDER, 
            font=font.Font(family=Config.MAIN_FONT, size=12)
        )
        folder_label.pack(side=tk.LEFT, padx=5)

        self.folder_path = tk.StringVar()
        self.folder_path.set(Config.DOWNLOAD_PATH)
        folder_entry = ttk.Entry(
            folder_frame, 
            textvariable=self.folder_path, 
            style="TEntry", 
            width=40
        )
        folder_entry.pack(side=tk.LEFT, padx=5)

        # download button and quality selection 
        button_frame = ttk.Frame(self.dl_container, style="TFrame")
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        download_button = ttk.Button(
            button_frame, 
            text=lang.DOWNLOAD, 
            style="Download.TButton", 
            takefocus=False, 
            command=self.start_download
        )
        download_button.pack(side=tk.LEFT, padx=5)

        self.options_list = create_video_dl_options(info)

        self.quality_var = tk.StringVar()
        self.quality_options = [option[0] for option in self.options_list]
        quality_dropdown = ttk.OptionMenu(
            button_frame, 
            self.quality_var, 
            self.quality_options[0], 
            *self.quality_options
        )
        quality_dropdown.pack(side=tk.LEFT, padx=5)
        
        def browse_folder():
            folder_selected = filedialog.askdirectory()
            if folder_selected:
                self.folder_path.set(folder_selected)
        
        folder_button = ttk.Button(
            folder_frame, 
            text=lang.BROWSE, 
            style="Browse.TButton", 
            command=browse_folder, 
            takefocus=False
        )
        folder_button.pack(side=tk.LEFT, padx=5)
        
        def audio_only_monitor():
            if audio_only_var.get():
                new_options_list = [option for option in self.options_list if option[0].startswith("audio") or option[0] == "Best audio"]
                new_quality_var = tk.StringVar()
                new_quality_options = [option[0] for option in new_options_list]
                quality_dropdown['menu'].delete(0, 'end')
                for option in new_quality_options:
                    quality_dropdown['menu'].add_command(label=option, command=tk._setit(new_quality_var, option))
                self.quality_var.set(new_quality_options[0])
            else:
                new_options_list = [option for option in self.options_list if not option[0].startswith("audio") and option[0] != "Best audio"]
                new_quality_var = tk.StringVar()
                new_quality_options = [option[0] for option in new_options_list]
                quality_dropdown['menu'].delete(0, 'end')
                for option in new_quality_options:
                    quality_dropdown['menu'].add_command(label=option, command=tk._setit(new_quality_var, option))
                self.quality_var.set(new_quality_options[0])
        
        # checkbox for audio only
        audio_only_var = tk.BooleanVar()
        audio_only_checkbox = ttk.Checkbutton(
            button_frame,
            text=lang.SHOW_AUDIO_ONLY,
            variable=audio_only_var,
            style="TCheckbutton", 
            command=audio_only_monitor
        )
        audio_only_checkbox.pack(side=tk.LEFT, padx=5)

        # init
        audio_only_monitor()

    def start_download(self):
        ydl_opts = self.options_list[self.quality_options.index(self.quality_var.get())][1]
        dl_path = self.folder_path.get()
        url = self.url
        self.reload_frame()

        main_thread = threading.Thread(target=download_by_options, args=(url, ydl_opts, dl_path))
        output_frame = ttk.Frame(self.dl_container, style="TFrame")
        output_frame.pack(fill=tk.BOTH, expand=True)

        output_text = tk.Text(
            output_frame, 
            font=(Config.OUTPUT_FONT, 10, 'bold'), 
            background="#181818", 
            foreground="#cccccc",
            height=20, 
            width=100, 
            state=tk.DISABLED
        )
        output_text.pack()
        
        def update_output():
            log = MyLogger.pull_logging()
            if log:
                output_text.config(state=tk.NORMAL)
                
                # Parse the log and add it to tk.Text
                parsed_log = parse_ansi_text(log)
                for text, color in parsed_log:
                    if color:
                        if not color in output_text.tag_names():
                            output_text.tag_config(color, foreground=color)
                        output_text.insert(tk.END, text, color)
                    else:
                        output_text.insert(tk.END, text)
                
                output_text.config(state=tk.DISABLED)
                output_text.see(tk.END)
                
        def update_thread():
            while True:
                update_output()
                if not main_thread.is_alive():
                    update_output()
                    break
                time.sleep(0.1)

        def monitor_thread():
            main_thread.join()
            self.change_loading_text(text=lang.DOWNLOAD_COMPLETE)
            empty_label = ttk.Label(output_frame, text="")
            empty_label.pack()
            open_folder_button = ttk.Button(
                output_frame,
                text=lang.OPEN_FOLDER,
                style="OpenFolder.TButton",
                command=lambda: os.startfile(dl_path),
                takefocus=False
            )
            open_folder_button.pack()

        main_thread.start()
        self.show_loading(text=lang.DOWNLOADING)
        threading.Thread(target=update_thread, daemon=True).start()
        threading.Thread(target=monitor_thread, daemon=True).start()

    def draw_dl_playlist(self, info: dict):
        lebel = ttk.Label(
            self.dl_container, 
            style="TLabel", 
            text=f"{lang.PLAYLIST_INFO.format(info['title'])}", 
            font=font.Font(family=Config.MAIN_FONT, size=14)
        )
        lebel.pack()

class SettingsPage:
    def __init__(self, parent_master: tk.Tk):
        frame = ttk.Frame(parent_master, style="TFrame")
        frame.pack(fill=tk.BOTH, expand=True)
        self.master = frame

    def create_widgets(self):
        self.lebel = ttk.Label(
            self.master, 
            style="TLabel", 
            text="", 
            font=font.Font(family=Config.MAIN_FONT, size=14)
        )
        self.lebel.pack(pady=20)
        self.lebel.config(text=f"{lang.TAB_2}")

class UpdatePage:
    def __init__(self, parent_master: tk.Tk):
        frame = ttk.Frame(parent_master, style="TFrame")
        frame.pack(fill=tk.BOTH, expand=True)
        self.master = frame

    def create_widgets(self):
        self.lebel = ttk.Label(
            self.master, 
            style="TLabel", 
            text="", 
            font=font.Font(family=Config.MAIN_FONT, size=14)
        )
        self.lebel.pack(pady=20)
        self.lebel.config(text=f"{lang.CHECK_FOR_UPDATE}")


