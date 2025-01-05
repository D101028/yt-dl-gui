import os
import requests

from yt_dlp import YoutubeDL

from app.lang import lang

class MyLogger:
    logging = ""

    @classmethod
    def debug(cls, msg):
        cls.logging += f"{msg}\n"
        print(f"{msg}")
    @classmethod
    def warning(cls, msg):
        cls.logging += f"WARNING: {msg}\n"
        print(f"WARNING: {msg}")
    @classmethod
    def error(cls, msg):
        cls.logging += f"ERROR: {msg}\n"
        print(f"ERROR: {msg}")

    @classmethod
    def get_logging(cls):
        """取得目前的紀錄"""
        return cls.logging
    @classmethod
    def pull_logging(cls):
        """取得目前的紀錄並清空"""
        result = cls.logging
        cls.clear_logging()
        return result
    @classmethod
    def clear_logging(cls):
        cls.logging = ""

def check_url_accessibility(url: str):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def analyze_url(url_or_id: str, check_accessibility=False) -> tuple[str, str] | None:
    playlist_or_video = None
    temp = None
    if "youtu.be" in url_or_id:
        playlist_or_video = "video"
        temp = url_or_id.split("/")[-1]
        if "?" in temp:
            temp = temp.split("?")[0]
    elif "?" in url_or_id:
        temp = url_or_id.split("?")[1]
        for arg in temp.split("&"):
            if arg.startswith("v="): # youtube video id
                temp = arg.split("=")[1]
                playlist_or_video = "video"
                break
            elif arg.startswith("list="): # youtube playlist id
                temp = arg.split("=")[1]
                playlist_or_video = "playlist"
                break
        else:
            return None
    else:
        # pure id
        if len(url_or_id) == 11: # youtube video id
            temp = url_or_id
            playlist_or_video = "video"
        else: # youtube playlist id
            temp = url_or_id
            playlist_or_video = "playlist"
    
    if not temp:
        return None

    if check_accessibility:
        url = f"https://www.youtube.com/watch?v={temp}" if playlist_or_video == "video" else f"https://www.youtube.com/playlist?list={temp}"
        if not check_url_accessibility(url):
            return None
    return playlist_or_video, temp

def get_video_info(url):
    ydl_opts = {
        'skip_download': True,
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)  # 不下載影片
    return info

def get_playlist_info(url):
    ydl_opts = {
        'extract_flat': True,  # 僅擷取清單資訊而不下載影片
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info

def download_thumbnail(url, path):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
        return path
    return None

def format_summary(info: dict) -> str:
    summaries = []
    for f in info['formats']:
        summary = {
            'format_id': f.get('format_id'),
            'format_note': f.get('format_note'),
            'resolution': f.get('resolution'),
            'fps': f.get('fps'),
            'vcodec': f.get('vcodec'),
            'acodec': f.get('acodec'),
            'filesize': f.get('filesize'),
            # 'url': f.get('url')
        }
        summaries.append(summary)

    return summaries

def create_video_dl_options(info: dict) -> list[tuple[str, dict]]:
    result = []
    result.append(("Best quality", {
        "format": "bestvideo+bestaudio/best", 
        "outtmpl": "%(title)s.%(ext)s", 
        "quiet": False, 
        "logger": MyLogger
    }))
    result.append(("Best audio", {
        "format": "bestaudio", 
        "outtmpl": "%(title)s.%(ext)s", 
        "quiet": False, 
        "postprocessors": [], 
        "logger": MyLogger
    }))

    summaries = format_summary(info)
    for summary in summaries:
        fmt = summary['format_id']
        if summary["resolution"] != "audio only":
            options = {
                "format": fmt,
                "outtmpl": "%(title)s.%(ext)s",
                "quiet": False, 
                "logger": MyLogger
            }
            result.append((f"{summary['resolution']}-{summary['format_note']}-{summary['format_id']}", options))
        else:
            options = {
                "format": fmt,
                "outtmpl": "%(title)s.%(ext)s",
                "quiet": False,
                "logger": MyLogger
            }
            result.append((f"audio-{summary['format_note']}-{summary['acodec']}-{summary['format_id']}", options))

    return result

def download_by_options(url: str, options: dict, dl_path: str):
    ydl_opts = options
    ydl_opts["outtmpl"] = os.path.join(dl_path, ydl_opts["outtmpl"])
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
