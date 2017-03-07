from pytube import YouTube

"""
Downloader is used to download video and provides functions to handle video properties
"""


class Downloader:
    def __init__(self, url):
        self.url = url

    # setUrl(url) updates the youTube url for the downloader
    # setUrl: self, String - > void
    def setUrl(self, url):
        self.url = url
