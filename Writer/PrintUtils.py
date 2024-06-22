import termcolor
import datetime
import os


def PrintMessageHistory(_Messages):
    print("------------------------------------------------------------")
    for Message in _Messages:
        print(Message)
    print("------------------------------------------------------------")


class Logger:

    def __init__(self, _LogfilePrefix="Logs/"):

        # Make Paths For Log
        try:
            os.makedirs(_LogfilePrefix)
        except FileExistsError:
            pass

        self.LogPath = _LogfilePrefix + "Log_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".log"
        self.File = open(self.LogPath, "a")

        self.LogItems = []

    def Log(self, _Item, _Level:int):

        # Create Log Entry
        LogEntry = f"[{str(_Level).ljust(2)}] [{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}] {_Item}"

        # Write it to file
        self.File.write(LogEntry + "\n")
        self.LogItems.append(LogEntry)

        # Now color and print it
        if (_Level == 0):
            LogEntry = termcolor.colored(LogEntry, "white")
        elif (_Level == 1):
            LogEntry = termcolor.colored(LogEntry, "grey")
        elif (_Level == 2):
            LogEntry = termcolor.colored(LogEntry, "blue")
        elif (_Level == 3):
            LogEntry = termcolor.colored(LogEntry, "cyan")
        elif (_Level == 4):
            LogEntry = termcolor.colored(LogEntry, "magenta")
        elif (_Level == 5):
            LogEntry = termcolor.colored(LogEntry, "green")
        elif (_Level == 6):
            LogEntry = termcolor.colored(LogEntry, "yellow")
        elif (_Level == 7):
            LogEntry = termcolor.colored(LogEntry, 7)

        print(LogEntry)



    def __del__(self):
        self.File.close()