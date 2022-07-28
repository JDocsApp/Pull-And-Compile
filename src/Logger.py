"""
Function for logging
"""
from datetime import datetime


class Logger:
    def __init__(self, path: str):
        """
        Constructor for the logger

        :param path: File to open and log to
        """
        self.path = path

        self.logFile = False

        try:
            self.file = open(self.path, "a+")
            self.logFile = True

        except:
            print("Could not open file, continuing logging without logging to file")

    def log(self, msg: str) -> None:
        """
        Log as print and to a file, stamp with time

        :param msg: Message to log
        """
        fullMsg = "{} == {}".format(datetime.now(), msg)
        print(fullMsg)

        if self.logFile:
            self.file.write(fullMsg + "\n")
            self.file.flush()

    def __del__(self):
        if self.logFile:
            self.file.close()
