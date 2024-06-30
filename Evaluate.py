#!/bin/python3

import argparse
import time
import json
import datetime
import os

import Writer.Interface.Wrapper
import Writer.Config
import Writer.PrintUtils


def GetNumChapters(_Client, _Logger, _Story):
    
    _Logger.Log("Detecting Num Chapters In Story", 4)
    Messages = [Interface.BuildSystemQuery("You are a helpful AI language model.")]
    Messages.append(Interface.BuildUserQuery(f"""
    I need to identify the number of chapters in the given story:
                                            
    <STORY>
    {Story}
    </STORY>

    Please respond with JSON as follows:
    {{
        "NumChapters": <NumChapters>
    }}

    Only respond with just JSON - your output will be parsed by a computer.
    
    """))
    Messages = Interface.ChatAndStreamResponse(Logger, Messages, Args.Model)
    JSON = Interface.GetLastMessageText(Messages)

    _Logger.Log("Finished Detecting Num Chapters In Story", 4)

    return json.loads(JSON)["NumChapters"]

def GetChapter(_Client, _Logger, _Story, _Chapter):
    
    _Logger.Log(f"Extracting Chapter {_Chapter} From Story", 4)
    Messages = [Interface.BuildSystemQuery("You are a helpful AI language model.")]
    Messages.append(Interface.BuildUserQuery(f"""
    Please extract chapter {_Chapter} from the following story:
                                            
    <STORY>
    {Story}
    </STORY>

    Only respond with the full story text for chapter {_Chapter} verbatim (not the outline). Do not include anything else in your response.
    
    """))
    Messages = Interface.ChatAndStreamResponse(Logger, Messages, Args.Model)
    _Logger.Log(f"Finished Extracting Chapter {_Chapter} From Story", 4)

    return Interface.GetLastMessageText(Messages)


# Setup Argparser
Parser = argparse.ArgumentParser()
Parser.add_argument("-Story", help="Path to file containing the story to evaluate")
Parser.add_argument("-Output", default="", type=str, help="Optional file output path, if none is specified, we will only print the rating to terminal",)
Parser.add_argument("-Host", default="localhost:11434", type=str, help="HTTP URL to OLLAMA instance",)
Parser.add_argument("-Model", default="llama3:70b", type=str, help="Model to use for writing the base outline content",)

Args = Parser.parse_args()

Writer.Config.OLLAMA_HOST = Args.Host


# Measure Generation Time
StartTime_s = time.time()

# Setup Logger
Logger = Writer.PrintUtils.Logger("EvalLogs")

# Setup Logger
Interface = Writer.Interface.Wrapper.Interface([Args.Model])

# Load the initial story
Story:str = ""
with open(Args.Story, "r") as f:
    Story = f.read()



ChapterCount = GetNumChapters(Interface, Logger, Story)

Chapters:list = []
for i in range(ChapterCount):
    Chapters.append(GetChapter(Interface, Logger, Story, i))



Messages = [Interface.BuildSystemQuery("You are a helpful AI language model.")]
Messages.append(Interface.BuildUserQuery(f"""
Please rate the below story:
                                          
<STORY>
{Story}
</STORY>

Please respond in the following categories:
- Plot: Does the story have a coherent plot? Is It creative?
- Chapters: Do the chapters flow into each-other (be very careful when checking this)? Do they feel connected? Do they feel homogenized or are they unique and fresh?
- Style: Does the writing style help move the plot or is it distracting from the rest of the story? Is it excessively flowery?
- Dialogue: Is the dialog specific to each character? Does it feel in-character? Is there enough or too little?
- Tropes: Do the tropes make sense for the genre? Are they interesting and well integrated?
- Genre: Is the genre clear?

"""))
Messages = Interface.ChatAndStreamResponse(Logger, Messages, Args.Model)


# Calculate Eval Time
EndTime_s = time.time()
TotalEvalTime_s = round(EndTime_s - StartTime_s)



# Build Report
Report:str = ""

# Optionally write Report To Disk
if (Args.Output != ""):
    with open(Args.Output, "w") as f:
        f.write(Report)





