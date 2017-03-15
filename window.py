from tkinter import *
from tkinter import ttk

"""
Window is a GUI used by user to download youtube video
"""


class Window:
    def __init__(self):
        # root for the window
        self.master = Tk()

        # make window non resizable and set the background color
        self.master.resizable(False, False)
        self.master.config(background = "#64b3d9")

        # set window title and icon
        self.master.title("Youtube Downloader")
        img = PhotoImage(file = r'icon.png')
        self.master.tk.call('wm', 'iconphoto', self.master._w, img)

        # set style for different components
        self.style = ttk.Style()
        self.style.configure("TFrame", background = "#64b3d9")
        self.style.configure("TButton", background = "#64b3d9", Font = ("Agency FB", 20))
        self.style.configure("TLabel", background = "#64b3d9", font = ("Agency FB", 20))

        self.frame = ttk.Frame(self.master)
        self.frame.pack()

        self.background = PhotoImage(file = "background.png")
        ttk.Label(self.frame, image = self.background).grid(row = 0, column = 0)

        # text field to get url
        self.text_field = ttk.Entry(self.frame, width = 45, style = "TEntry")
        self.text_field.place(x = 20, y = 180)

        # search button
        self.search_btn = ttk.Button(self.frame, text = "Search")
        self.search_btn.place(x = 310, y = 178)

        # download video button
        self.video_btn = ttk.Button(self.frame, text = "Download Video")
        self.video_btn.place(x = 90, y = 460)
        self.audio_btn = ttk.Button(self.frame, text = "Download Audio")
        self.audio_btn.place(x = 220, y = 460)

        # download audio button
        self.status = ttk.Label(self.frame, wraplength = 350, text = "Type Url of the video that you want to download!")
        self.status.config(foreground = "white")
        self.status.place(x = 35, y = 510)

        # labels to show video information
        self.title_label = ttk.Label(self.frame, text = "")
        self.title_label.place(x = 150, y = 234)

        self.author_label = ttk.Label(self.frame, text = "")
        self.author_label.place(x = 150, y = 287)

        self.views_label = ttk.Label(self.frame, text = "")
        self.views_label.place(x = 150, y = 340)

        self.length_label = ttk.Label(self.frame, text = "")
        self.length_label.place(x = 150, y = 392)

        self.master.mainloop()
