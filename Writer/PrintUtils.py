import termcolor
import datetime
import os
import json


def PrintMessageHistory(_Messages):
    print("------------------------------------------------------------")
    for Message in _Messages:
        print(Message)
    print("------------------------------------------------------------")


class Logger:

    def __init__(self, _LogfilePrefix="Logs/"):

        # Make Paths For Log
        LogDirPath = _LogfilePrefix + "/Log_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "/LangchainDebug"
        os.makedirs(_LogfilePrefix, exist_ok=True)

        # Setup Log Path
        self.LogDirPrefix = LogDirPath
        self.LogPath = LogDirPath + "/Main.log"
        self.File = open(self.LogPath, "a")
        self.LangchainID = 0

        self.LogItems = []


    # Helper function that saves the entire language chain object as both json and markdown for debugging later
    def SaveLangchain(self, _LangChainID:str, _LangChain:list):

        # Calculate Filepath For This Langchain
        ThisLogPathJSON:str = self.LogDirPrefix + f"/LangchainDebug/{_LangChainID}_{self.LangchainID}.json"
        ThisLogPathMD:str = self.LogDirPrefix + f"/LangchainDebug/{_LangChainID}_{self.LangchainID}.md"
        LangChainDebugTitle:str = f"{_LangChainID}_{self.LangchainID}"
        self.LangchainID += 1

        # Generate and Save JSON Version
        with open(ThisLogPathJSON, "w") as f:
            f.write(json.dumps(_LangChain, indent=4, sort_keys=True))
        
        # Now, Save Markdown Version
        with open(ThisLogPathMD, "w") as f:
            MarkdownVersion:str = f"# Debug LangChain {LangChainDebugTitle}\n"
            for Message in _LangChain:
                MarkdownVersion += f"\n\n\n## Role: {Message['role']}\n"
                MarkdownVersion += f"{Message['content']}"
            f.write(MarkdownVersion)
        
        self.Log(f"Wrote This Language Chain ({LangChainDebugTitle}) To Debug File {ThisLogPathMD}", 5)


    # Saves the given story to disk
    def SaveStory(self, _StoryContent:str):

        with open(f"{self.LogDirPrefix}/Story.md", "w") as f:
            f.write(_StoryContent)

        self.Log(f"Wrote Story To Disk At {self.LogDirPrefix}/Story.md", 5)


    # Logs an item
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
            LogEntry = termcolor.colored(LogEntry, "red")

        print(LogEntry)



    def __del__(self):
        self.File.close()