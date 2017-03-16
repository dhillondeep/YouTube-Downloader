from tkinter import *
from tkinter import ttk
from downloader import Downloader
from tkinter import filedialog
import threading

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
        self.style.configure("TButton", background = "#64b3d9", Font = ("Agency FB", 20))
        self.style.configure("TLabel", background = "#64b3d9", font = ("Agency FB", 15))
        self.style.configure("S.TLabel", background = "#64b3d9", font = ("Agency FB", 20))

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
        self.video_btn.place(x = 90, y = 470)

        # download audio button
        self.audio_btn = ttk.Button(self.frame, text = "Download Audio")
        self.audio_btn.place(x = 220, y = 470)

        # status label
        self.status = ttk.Label(self.frame, wraplength = 350, text = "Type Url of the video that you want to download!")
        self.status.config(foreground = "white", style="S.TLabel")
        self.status.place(x = 35, y = 510)

        # labels to show video information
        self.title_label = ttk.Label(self.frame, text = "", wraplength = 200)
        self.title_label.place(x = 150, y = 234)

        self.author_label = ttk.Label(self.frame, text = "")
        self.author_label.place(x = 150, y = 312)

        self.views_label = ttk.Label(self.frame, text = "")
        self.views_label.place(x = 150, y = 365)

        self.length_label = ttk.Label(self.frame, text = "")
        self.length_label.place(x = 150, y = 415)

        # disable all the buttons except search
        self.video_btn.config(state=DISABLED)
        self.audio_btn.config(state=DISABLED)

        # add event listeners to buttons
        self.search_btn.config(command = self.searchAction)
        self.video_btn.config(command = self.videoAction)
        self.audio_btn.config(command = self.audioAction)

        # download thread
        self.search_thread = None
        self.downloadV_thread = None
        self.downloadA_thread = None

        # other variables
        self.video_searched = False
        self.video_downloaded = False
        self.audio_downloaded = False

        self.master.mainloop()

    def actions(self):
        if self.search_thread is not None:
            if not self.search_thread.isAlive() and not self.video_searched:
                if self.downloader.data_aquired:
                    self.title_label.config(text=self.downloader.getTitle())
                    self.author_label.config(text=self.downloader.getAuthor())
                    self.views_label.config(text=self.downloader.getViews())
                    self.length_label.config(text=self.downloader.getTime())
                    self.status.config(text = "Video Successfully Searched")
                    self.video_searched = True

                    # enable download buttons
                    self.video_btn.config(state=NORMAL)
                    self.audio_btn.config(state=NORMAL)
                else:
                    self.status.config(text="Error occurred while searching")

        if self.downloadV_thread is not None:
            if not self.downloadV_thread.isAlive() and not self.video_downloaded:
                if self.downloader.video_downloaded:
                    print("GG")
                    self.video_downloaded = True
                else:
                    print("No GG")

        self.master.after(1000, self.actions)

    def searchAction(self):
        # get text from text field
        value = self.text_field.get()

        if value != "":
            self.downloader.setUrl(value)
            self.search_thread = threading.Thread(target=self.downloader.getVideoData)
            self.search_thread.start()

            self.video_searched = False
            self.status.config(text="Searching for the video")

    def videoAction(self):
        location = filedialog.askdirectory()

        if location != "":
            print("Location: ", location)
            self.downloader.setLocation(location)
            #self.downloadV_thread = threading.Thread(target=self.downloader.downloadVideo)
            self.downloader.downloadVideo()
            self.video_downloaded = False

    def audioAction(self):
        pass


def main():
    d = Downloader(None)
    w = Window(d)


if __name__ == '__main__':
    main()


