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
    Messages = Interface.SafeGenerateText(Logger, Messages, Args.Model)
    JSON = Interface.GetLastMessageText(Messages)

    _Logger.Log("Finished Detecting Num Chapters In Story", 4)

    return json.loads(JSON)["NumChapters"]

def GetChapter(_Client, _Logger, _Story, _Chapter):
    
    _Logger.Log(f"Extracting Chapter {_Chapter} From Story", 4)
    Messages = [Interface.BuildSystemQuery("You are a helpful AI language model.")]
    Messages.append(Interface.BuildUserQuery(f"""
    Please extract chapter {_Chapter} from the following story:
                                            
    <STORY>
    {_Story}
    </STORY>

    Copy the full chapter text for chapter {_Chapter}. Don't summarize or change any details, just copy the whole thing exactly as it's written.

    This should be several thousand words at least.
    
    """))
    Messages = Interface.SafeGenerateText(Logger, Messages, Args.Model)
    _Logger.Log(f"Finished Extracting Chapter {_Chapter} From Story", 4)

    return Interface.GetLastMessageText(Messages)


def EvaluateOutline(_Client, _Logger, _Outline1, _Outline2):
    
    _Logger.Log(f"Evaluating Outlines From Story", 4)
    Messages = [_Client.BuildSystemQuery("You are a helpful AI language model.")]
    Messages.append(_Client.BuildUserQuery(f"""
Please evaluate which outlines are better from the following two outlines:

Here's the first outline:
<Outline1>
{_Outline1}
</Outline1>

And here is the second outline:
<Outline2>
{_Outline2}
</Outline2>

Use the following criteria to evaluate (NOTE: You'll be picking outline 1 or outline 2 later on for these criteria):
- Plot: Does the story have a coherent plot? Is It creative?
- Chapters: Do the chapters flow into each-other (be very careful when checking this)? Do they feel connected? Do they feel homogenized or are they unique and fresh?
- Style: Does the writing style help move the plot or is it distracting from the rest of the story? Is it excessively flowery?
- Dialogue: Is the dialog specific to each character? Does it feel in-character? Is there enough or too little?
- Tropes: Do the tropes make sense for the genre? Are they interesting and well integrated?
- Genre: Is the genre clear?
- Narrative Structure: Is it clear what the structure is? Does it fit with the genre/tropes/content?

Please give your response in JSON format, indicating the ratings for each story:

{{
    "Plot": <1 or 2>,
    "Chapters: <1 or 2>,
    "Style": <1 or 2>,
    "Dialogue": <1 or 2>,
    "Tropes": <1 or 2>,
    "Genre": <1 or 2>,
    "Narrative": <1 or 2>,
    "OverallWinner": <1 or 2>
}}
    
Do not respond with anything except JSON.
    """))
    Messages = _Client.SafeGenerateText(Logger, Messages, Args.Model)
    JSON = json.loads(_Client.GetLastMessageText(Messages))
    Report = ""
    Report += f"Winner of Plot: {JSON['Plot']}\n"
    Report += f"Winner of Chapters: {JSON['Chapters']}\n"
    Report += f"Winner of Style: {JSON['Style']}\n"
    Report += f"Winner of Dialogue: {JSON['Dialogue']}\n"
    Report += f"Winner of Tropes: {JSON['Tropes']}\n"
    Report += f"Winner of Genre: {JSON['Genre']}\n"
    Report += f"Winner of Narrative: {JSON['Narrative']}\n"
    Report += f"Overall Winner: {JSON['OverallWinner']}\n"
    
    _Logger.Log(f"Finished Evaluating Outlines From Story", 4)

    return Report




# Setup Argparser
Parser = argparse.ArgumentParser()
Parser.add_argument("-Story1", help="Path to JSON file for story 1")
Parser.add_argument("-Story2", help="Path to JSON file for story 2")
Parser.add_argument("-Output", default="", type=str, help="Optional file output path, if none is specified, we will only print the rating to terminal",)
Parser.add_argument("-Host", default="localhost:11434", type=str, help="HTTP URL to OLLAMA instance",)
Parser.add_argument("-Model", default="llama3:70b", type=str, help="Model to use for writing the base outline content",)

Args = Parser.parse_args()

Writer.Config.OLLAMA_HOST = Args.Host
Writer.Config.DEBUG = True


# Measure Generation Time
StartTime_s = time.time()

# Setup Logger
Logger = Writer.PrintUtils.Logger("EvalLogs")

# Setup Logger
Interface = Writer.Interface.Wrapper.Interface([Args.Model])

# Load the initial story
Story1:dict = {}
Story2:dict = {}
with open(Args.Story1, "r") as f:
    Story1 = json.loads(f.read())
with open(Args.Story2, "r") as f:
    Story2 = json.loads(f.read())


# ChapterCount = GetNumChapters(Interface, Logger, Story)

# Chapters:list = []
# for i in range(1, ChapterCount + 1):
#     Chapters.append(GetChapter(Interface, Logger, Story, i))

# Begin Report
Report:str = "# Story Evaluation Report\n\n"
Report += f"Story 1: {Args.Story1}\n"
Report += f"Story 2: {Args.Story2}\n\n\n"

## Evaluate Outlines
Report += f"## Outline"
Report += EvaluateOutline(Interface, Logger, Story1["Outline"], Story2["Outline"])

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
Messages = Interface.SafeGenerateText(Logger, Messages, Args.Model)


# Calculate Eval Time
EndTime_s = time.time()
TotalEvalTime_s = round(EndTime_s - StartTime_s)



# Build Report
Report:str = ""

# Optionally write Report To Disk
if (Args.Output != ""):
    with open(Args.Output, "w") as f:
        f.write(Report)





