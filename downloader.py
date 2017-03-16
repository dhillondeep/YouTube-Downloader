from pytube import YouTube
from pytube.exceptions import DoesNotExist
import threading

"""
Downloader is used to download video and provides functions to handle video properties.
Downloader will download files using different thread
"""


class Downloader:
    def __init__(self, url):
        self._url = url
        self._videos = None
        self._video_data = None
        self._youTube = YouTube(url)
        self._h_video = None
        self._location = None

        # boolean to keep track when video is downloaded
        self._data_acquired = False
        self._video_downloaded = False
        self._videos_downloaded = False
        self._video_saved = False

        self._createYoutube(self._url)

    # _createYoutube(url) creates YouTube object using url so that videos can be
    # downloaded
    # _createYoutube: self, String -> void
    # effect: modifies _youtube
    def _createYoutube(self, url):
        self._youTube = YouTube(url)

    # downloadVideos() downloads the videos and store them in a list
    # downloadVideo: self -> void
    # effect: calls a function that modifies variables
    def downloadVideos(self):
        threading.Thread(target = self._getVideos).start()

    # _downloadVideos() download videos and store them in a list. This runs on
    # a separate thread and hence should not be called by user.
    # _downloadVideos: self -> void
    # effects: changes value of _videos_downloaded boolean and _videos
    def _getVideos(self):
        # download videos and store them
        try:
            self._videos = self._youTube.get_videos()
            self._videos_downloaded = True
        except DoesNotExist:
            self._videos_downloaded = False

    # downloadVideoData() gathers important data for the video and stores it in
    # dictionary.
    # downloadVideoData: self -> void
    # effects: calls a function that modifies variables
    def downloadVideoData(self):
        threading.Thread(target = self._getVideoData()).start()

    # _getVideoData() gathers important data for the video and stores in dictionary.
    # This function is protected and hence runs on thread and shouldn't be called.
    # _getVideoData: self -> Void
    # effect: changes value of _data_acquired boolean, _video_data
    def _getVideoData(self):
        # name: author
        # length: length_seconds
        # views: view_count
        # rating: avg_rating
        # title: title

        try:
            data = self.youTube.get_video_data()
            args = data["args"]

            self._video_data = {"author": args["author"],
                                "length": args["length_seconds"],
                                "views": args["view_count"],
                                "rating": args["avg_rating"],
                                "title": args["title"]}
            self._data_acquired = True
        except DoesNotExist:
            self._data_acquired = False

    # downloadBestVideo() downloads the highest quality video and stores it
    # downloadBestVideo: self -> void
    # effect: calls a function that modifies variables
    def downloadBestVideo(self):
        threading.Thread(target = self._getHighestVideo).start()

    # _getHighestVideo() returns the highest quality video. This runs on a thread
    # and hence should not be called by user
    # _getHighestVideo: self -> void
    # effects: changes value of _video_downloaded boolean and _video
    def _getHighestVideo(self):
        video = None
        gotten = True

        # 720p video
        try:
            video = self._youTube.get('mp4', '720p')
            gotten = True
        except DoesNotExist:
            gotten = False

        # 480p video
        if not gotten:
            try:
                video = self._youTube.get('mp4', '480p')
                gotten = True
            except DoesNotExist:
                gotten = False

        # 360p video
        if not gotten:
            try:
                video = self._youTube.get('mp4', '360p')
                gotten = True
            except DoesNotExist:
                gotten = False

        # 240p video
        if not gotten:
            try:
                video = self._youTube.get('mp4', '240p')
                gotten = True
            except DoesNotExist:
                gotten = False

        if gotten:
            self._video = video
            self._video_downloaded = True
        else:
            self._video_downloaded = False

    # saveVideo(location) saves the best resolution video at the location
    # saveVideo: self -> Void
    # effects: changes value of _location and calls a function that modifies variables
    def saveVideo(self, location):
        self._location = location

        threading.Thread(target = self._save).start()

    # _save() saves the best resolution video at the location. It runs on a separate
    # and hence should not be called by user
    # save: self -> void
    # effects: changes value of _video_saved boolean
    def _save(self):
        print("Saving video")
        try:
            self.video.download(self._location)
            self._video_saved = True
        except DoesNotExist:
            self._video_saved = False

    # setUrl(url) updates the youTube url for the downloader
    # setUrl: self, String - > void
    # effect: changes value of _url and calls a function
    def setUrl(self, url):
        self._url = url
        self._createYoutube(self._url)

    # getTime() returns the time in hours, minutes and seconds
    # getTime: self -> string
    def getTime(self):
        time_sec = int(self._video_data["length"])
        seconds = int(time_sec % 60)
        minutes = time_sec / 60
        hours = int(minutes / 60)
        minutes = int(minutes - (hours * 60))

        if hours != 0:
            return "{}:{}:{}".format(hours, minutes, seconds)
        else:
            return "{}:{}".format(minutes, seconds)

    # getAuthor() returns the name of the author of the video
    # getAuthor: self -> string
    def getAuthor(self):
        return self._video_data["author"]

    # getViews() returns the view count of the video
    # getViews: self -> int
    def getViews(self):
        return self._video_data["views"]

    # getRating() returns the rating of the video
    # getRating: self -> float
    def getRating(self):
        return self._video_data["rating"]

    # getTitle() returns the title of the video
    # getTitle: self -> String
    def getTitle(self):
        return self._video_data["title"]

    # isDataAcquired() returns true if data is acquired and false otherwise
    # isDataAcquired: self -> boolean
    def isDataAcquired(self):
        return self._data_acquired

    # isVideoDownloaded() returns true if best quality video is downloaded and false otherwise
    # isVideoDownloaded: self -> boolean
    def isVideoDownloaded(self):
        return self._video_downloaded

    # areVideosDownloaded() returns true if videos are downloaded and false otherwise
    # areVideosDownloaded: self -> boolean
    def areVideosDownloaded(self):
        return self._videos_downloaded

    # isVideoSaved() returns true if best quality video is saved and false otherwise
    # isVideoSaved: self -> boolean
    def isVideoSaved(self):
        return self._video_saved
