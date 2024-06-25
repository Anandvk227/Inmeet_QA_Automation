import configparser
import os

config=configparser.RawConfigParser()
config.read(os.path.join("Configurations", "config.ini"))

# config=configparser.RawConfigParser()
# config.read(".\\Configurations\\config.ini")

class ReadConfig:
    @staticmethod
    def getApplicationURL():
        url=config.get('common info','baseURL')
        return url

    @staticmethod
    def getUseremail():
        username=config.get('common info','useremail')
        return username

    @staticmethod
    def getPassword():
        password=config.get('common info','password')
        return password

# ==================Krishna==============================
    @staticmethod
    def getwhats():
        whats = config.get('common info', 'whats')
        return whats

    @staticmethod
    def getuseremails():
        usernames = config.get('common info', 'useremails')
        return usernames

    @staticmethod
    def getwhatso():
        whatso = config.get('common info', 'whatso')
        return whatso

    @staticmethod
    def getuseremails1():
        usernames1 = config.get('common info', 'useremails1')
        return usernames1

    @staticmethod
    def getuseremails2():
        usernames2 = config.get('common info', 'useremails2')
        return usernames2

    @staticmethod
    def getuseremails3():
        usernames3 = config.get('common info', 'useremails3')
        return usernames3

    @staticmethod
    def getwhatson():
        whatson = config.get('common info', 'whatson')
        return whatson

    @staticmethod
    def getgallery():
        gallery = config.get('common info', 'gallery')
        return gallery

    @staticmethod
    def getoneimage():
        oneimage = config.get('common info', 'oneimage')
        return oneimage

    @staticmethod
    def getfiveimages():
        fiveimages = config.get('common info', 'fiveimages')
        return fiveimages

    @staticmethod
    def getwhatvideo():
        whatvideo = config.get('common info', 'whatvideo')
        return whatvideo

    @staticmethod
    def getwhatvideos():
        whatvideos = config.get('common info', 'whatvideos')
        return whatvideos

    @staticmethod
    def getwhatyoutube():
        whatyoutube = config.get('common info', 'whatyoutube')
        return whatyoutube

    @staticmethod
    def getyoutubeurl():
        youtubeurl = config.get('common info', 'youtubeurl')
        return youtubeurl

    @staticmethod
    def getwhatedit():
        whatedit = config.get('common info', 'whatedit')
        return whatedit
