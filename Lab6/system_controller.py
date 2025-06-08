from Lab3.Lab3 import Logger

class SystemController:
    def __init__(self, logger: Logger):
        self.text = ''
        self.volume = 50
        self.media_playing = False
        self.logger = logger

    def log(self, message: str):
        self.logger.log(message)