from tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk

# 初始化 Tkinter 窗口
root = Tk()
root.title("Tkinter 使用 ttf 字型")

# 建立畫布
canvas = Canvas(root, width=400, height=300)
canvas.pack()

# 加載字型檔案
font_path = "font/CONSOLA.TTF"  # 替換成你的 .ttf 檔案路徑
font = ImageFont.truetype(font_path, 30)

# 建立 Pillow 圖像來渲染文字
image = Image.new("RGB", (400, 300), color="white")
draw = ImageDraw.Draw(image)
draw.text((50, 100), "使用 ttf 字型", font=font, fill="black")

# 將 Pillow 圖像轉換為 Tkinter 圖像
tk_image = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor=NW, image=tk_image)

root.mainloop()
