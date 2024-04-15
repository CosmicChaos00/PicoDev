class Constant:
    @staticmethod
    def getURL():
        URL = "https://us-east-2.aws.data.mongodb-api.com/app/data-qzajs/endpoint/data/v1/action/"
        return URL
    @staticmethod
    def getAPI_KEY():
        API_KEY = "KBQ0COPf87LPexT8QYcKj2Zz5Ll626USLubuNJtFbX1aElYzVJO876Zu0lISmB7e"
        return API_KEY
    @staticmethod
    def getHubURL():
        BASE_URL='https://raw.githubusercontent.com/CosmicChaos00/PicoDev/master'
        return BASE_URL
    
    @staticmethod
    def getAPI_URL():
        GIT_API_URL='https://api.github.com/repos/CosmicChaos00/PicoDev/commits?path='
        return GIT_API_URL
    @staticmethod
    def getToken():
        TOKEN = "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"
        return TOKEN
    @staticmethod
    def getOwner():
        OWNER = "CosmicChaos00"
        return OWNER    
    @staticmethod
    def getRepo():
        REPO = "PicoDev"
        return REPO
    
    @staticmethod
    def getFiles():
        FILES = ["constantData.py","imu.py,main.py","Pico.py","update.py","vector3d.py","vectorMagnitude.py","wifi.txt","wifi.py"]
        return FILES
    
    #github api_token
    @staticmethod
    def getVersionPath():
        version_file_path = "version/version.txt"
        return version_file_path
    
    @staticmethod
    def getLocalVersion_path():
        local_file_path = "local_version.txt"
        return local_file_path
        

