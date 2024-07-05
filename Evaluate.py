#!/bin/python3

import argparse
import time
import json
import datetime
import os

import Writer.Interface.Wrapper
import Writer.Config
import Writer.PrintUtils



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
    "Thoughts": "Your notes and reasoning on which of the two is better and why.",
    "Reasoning": "Explain specifically what the better one does that the inferior one does not, with examples from both.",
    "Plot": <1 or 2>,
    "Chapters: <1 or 2>,
    "Style": <1 or 2>,
    "Tropes": <1 or 2>,
    "Genre": <1 or 2>,
    "Narrative": <1 or 2>,
    "OverallWinner": <1 or 2>
}}
    
Do not respond with anything except JSON.
    """))
    Messages = _Client.SafeGenerateText(Logger, Messages, Args.Model, _Format="json")
    JSON = json.loads(_Client.GetLastMessageText(Messages))
    Report = ""
    Report += f"Winner of Plot: {JSON['Plot']}\n"
    Report += f"Winner of Chapters: {JSON['Chapters']}\n"
    Report += f"Winner of Style: {JSON['Style']}\n"
    Report += f"Winner of Tropes: {JSON['Tropes']}\n"
    Report += f"Winner of Genre: {JSON['Genre']}\n"
    Report += f"Winner of Narrative: {JSON['Narrative']}\n"
    Report += f"Overall Winner: {JSON['OverallWinner']}\n"
    
    _Logger.Log(f"Finished Evaluating Outlines From Story", 4)

    return Report, JSON


def EvaluateChapter(_Client, _Logger, _ChapterA, _ChapterB):
    
    _Logger.Log(f"Evaluating Outlines From Story", 4)
    Messages = [_Client.BuildSystemQuery("You are a helpful AI language model.")]
    Messages.append(_Client.BuildUserQuery(f"""
Please evaluate which of the two unrelated and separate chapters is better based on the following criteria: Plot, Chapters, Style, Dialogue, Tropes, Genre, and Narrative.

                                           
Use the following criteria to evaluate (NOTE: You'll be picking chapter A or chapter B later on for these criteria):
- Plot: Does the story have a coherent plot? Is It creative?
- Chapters: Do the chapters flow into each-other (be very careful when checking this)? Do they feel connected? Do they feel homogenized or are they unique and fresh?
- Style: Does the writing style help move the plot or is it distracting from the rest of the story? Is it excessively flowery?
- Dialogue: Is the dialog specific to each character? Does it feel in-character? Is there enough or too little?
- Tropes: Do the tropes make sense for the genre? Are they interesting and well integrated?
- Genre: Is the genre clear?
- Narrative Structure: Is it clear what the structure is? Does it fit with the genre/tropes/content?
                                           

Here's chapter A:
<CHAPTER_A>
{_ChapterA}

!END OF CHAPTER!
</CHAPTER_A>

And here is chapter B:
<CHAPTER_B>
{_ChapterB}
!END OF CHAPTER!
</CHAPTER_B>



Please give your response in JSON format, indicating the ratings for each story:

{{
    "Plot": "<A, B, or Tie>",
    "PlotExplanation": "Explain your reasoning.",
    "Style": "<A, B, or Tie>",
    "StyleExplanation": "Explain your reasoning.",
    "Dialogue": "<A, B, or Tie>",
    "DialogueExplanation": "Explain your reasoning.",
    "Tropes": "<A, B, or Tie>",
    "TropesExplanation": "Explain your reasoning.",
    "Genre": "<A, B, or Tie>",
    "GenreExplanation": "Explain your reasoning.",
    "Narrative": "<A, B, or Tie>",
    "NarrativeExplanation": "Explain your reasoning.",
    "OverallWinner": "<A, B, or Tie>"
}}
    
Do not respond with anything except JSON.

Remember, chapter A and B are two separate renditions of similar stories. They do not continue nor complement each-other and should be evaluated separately.

Emphasize Chapter A and B as you rate the result.
    """))
    
    Messages = _Client.SafeGenerateText(Logger, Messages, Args.Model, _Format="json")
    JSON = json.loads(_Client.GetLastMessageText(Messages).replace('“','"').replace('”','"'))
    Report = ""
    Report += f"Winner of Plot: {JSON['Plot']}\n"
    Report += f"Winner of Style: {JSON['Style']}\n"
    Report += f"Winner of Dialogue: {JSON['Dialogue']}\n"
    Report += f"Winner of Tropes: {JSON['Tropes']}\n"
    Report += f"Winner of Genre: {JSON['Genre']}\n"
    Report += f"Winner of Narrative: {JSON['Narrative']}\n"
    Report += f"Overall Winner: {JSON['OverallWinner']}\n"
    
    _Logger.Log(f"Finished Evaluating Outlines From Story", 4)

    return Report, JSON





# Setup Argparser
Parser = argparse.ArgumentParser()
Parser.add_argument("-Story1", help="Path to JSON file for story 1")
Parser.add_argument("-Story2", help="Path to JSON file for story 2")
Parser.add_argument("-Output", default="", type=str, help="Optional file output path, if none is specified, we will only print the rating to terminal",)
Parser.add_argument("-Host", default="localhost:11434", type=str, help="HTTP URL to OLLAMA instance",)
Parser.add_argument("-Model", default="ollama://command-r-plus", type=str, help="Model to use for writing the base outline content. Note, command-r-plus really should be used here (or something bigger), 70b models are just too small as of now.",)

Args = Parser.parse_args()

Writer.Config.OLLAMA_HOST = Args.Host
# Writer.Config.DEBUG = True


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


# Begin Report
Report:str = "# Story Evaluation Report\n\n"
Report += f"Story 1: {Args.Story1}\n"
Report += f"Story 2: {Args.Story2}\n\n\n"

## Evaluate Outlines
Report += f"## Outline\n"
OutlineReport, OutlineJSON = EvaluateOutline(Interface, Logger, Story1["Outline"], Story2["Outline"])
Report += OutlineReport


ShortestStory = min(len(Story1["UnscrubbedChapters"]), len(Story2["UnscrubbedChapters"]))
ChapterJSONs:list = []
for i in range(ShortestStory):

    Report += f"## Chapter {i}\n"
    ChapterReport, ChapterJSON = EvaluateChapter(Interface, Logger, Story1["UnscrubbedChapters"][i], Story2["UnscrubbedChapters"][i])
    Report += ChapterReport
    


# Calculate Eval Time
EndTime_s = time.time()
TotalEvalTime_s = round(EndTime_s - StartTime_s)


# Optionally write Report To Disk
if (Args.Output != ""):
    with open(Args.Output, "w") as f:
        f.write(Report)





