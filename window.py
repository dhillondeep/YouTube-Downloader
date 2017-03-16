from tkinter import *
from tkinter import ttk
from tkinter import filedialog

"""
Window is a GUI used by user to download youtube video
"""


class Window:
    def __init__(self, downloader):
        # store downloader
        self.downloader = downloader

        # root for the window
        self.master = Tk()

        self.master.after(1000, self.actions)

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
        self.style.configure("TButton", background = "#64b3d9", font=("Segoe UI", 12))
        self.style.configure("TLabel", background = "#64b3d9", font = ("Agency FB", 15))
        self.style.configure("S.TLabel", background = "#64b3d9", font = ("Agency FB", 20))

        self.frame = ttk.Frame(self.master)
        self.frame.pack()

        self.background = PhotoImage(file = "background.png")
        ttk.Label(self.frame, image = self.background).grid(row = 0, column = 0)

        # text field to get url
        self.text_field = ttk.Entry(self.frame, width = 40)
        self.text_field.place(x = 20, y = 180)

        # search button
        self.search_btn = ttk.Button(self.frame, text = "Search")
        self.search_btn.place(x = 280, y = 175)

        # download video button
        self.video_btn = ttk.Button(self.frame, text = "Download Video")
        self.video_btn.place(x = 145, y = 470)

        # status label
        self.status = ttk.Label(self.frame, wraplength = 350, text = "Type Url of the video that you want to download!")
        self.status.config(foreground = "white", style="S.TLabel")
        self.status.place(x = 35, y = 510)

        # labels to show video information
        self.title_label = ttk.Label(self.frame, text = "", wraplength = 260, foreground = "white")
        self.title_label.place(x = 130, y = 234)

        self.author_label = ttk.Label(self.frame, text = "", wraplength = 260, foreground = "white")
        self.author_label.place(x = 130, y = 312)

        self.views_label = ttk.Label(self.frame, text = "", wraplength = 260, foreground = "white")
        self.views_label.place(x = 130, y = 365)

        self.length_label = ttk.Label(self.frame, text = "", wraplength = 260, foreground = "white")
        self.length_label.place(x = 130, y = 415)

        # disable all the buttons except search
        self.video_btn.config(state=DISABLED)

        # add event listeners to buttons
        self.search_btn.config(command = self.searchAction)
        self.video_btn.config(command = self.videoAction)

        # video location
        self.location = None
        self.saving = False

        self.master.mainloop()

    # actions() runs a loop along size mainloop every 1s and checks of
    # actions to be performed. The actions that were pending and now
    # complete are executed here
    # actions: self -> void
    def actions(self):
        # when data download finishes
        if self.downloader.isFinished(self.downloader.DATA):
            if not self.downloader.errorOccurred(self.downloader.DATA):
                self.title_label.config(text = self.downloader.getTitle())
                self.author_label.config(text = self.downloader.getAuthor())
                self.views_label.config(text = self.downloader.getViews())
                self.length_label.config(text = self.downloader.getTime())
                self.status.config(text = "Video Successfully Searched")

                # unblock buttons
                self.video_btn.config(state = "Normal")
            else:
                self.status.config(text = "Error occurred while searching")

            # reset
            self.downloader.resetThreadReport(self.downloader.DATA)

        # when video download finishes
        if self.downloader.isFinished(self.downloader.VIDEO):
            if not self.downloader.errorOccurred(self.downloader.VIDEO):
                if not self.saving:
                    self.downloader.saveVideo(self.location)
                    self.saving = True
                    self.status.config(text = "Saving Video")
            else:
                self.status.config(text = "Error occurred while downloading video")

            # reset
            self.downloader.resetThreadReport(self.downloader.VIDEO)

        # when video saving finishes
        if self.downloader.isFinished(self.downloader.SAVED):
            self.saving = False
            if not self.downloader.errorOccurred(self.downloader.SAVED):
                self.status.config(text = "Video Successfully Saved")
            else:
                self.status.config(text = "Could not Save Video")

            # reset
                self.downloader.resetThreadReport(self.downloader.SAVED)

        self.master.after(1000, self.actions)

    # searchAction() performs commands when search button is clicked
    # searchAction: self -> void
    def searchAction(self):
        # get text from text field
        value = self.text_field.get()

        if value != "":
            self.downloader.setUrl(value)
            self.downloader.downloadVideoData()
            self.status.config(text="Searching for the video")

    # videoAction() performs commands when download video button is clicked
    # videoAction: self -> void
    def videoAction(self):
        location = filedialog.askdirectory()
        self.location = location
        self.downloader.downloadBestVideo()
        self.status.config(text = "Downloading video")
