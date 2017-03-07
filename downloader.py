from pytube import YouTube

"""
Downloader is used to download video and provides functions to handle video properties
"""


class Downloader:
    def __init__(self, url):
        self.url = url
        self.videos = None

        try:
            self.youTube = YouTube(url)
            self.isValid = True
        except:
            self.isValid = False

    # setUrl(url) updates the youTube url for the downloader
    # setUrl: self, String - > void
    def setUrl(self, url):
        self.url = url

        try:
            self.youTube = YouTube(url)
            self.isValid = True
        except:
            self.isValid = False


