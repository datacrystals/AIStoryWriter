#!/bin/python3

import argparse
import time
import datetime

import Writer.Config
import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.ChapterDetector
import Writer.Scrubber
import Writer.Statistics
import Writer.OutlineGenerator
import Writer.StoryInfo
import Writer.NovelEditor


# Setup Argparser
Parser = argparse.ArgumentParser()
Parser.add_argument("-Prompt", help="Path to file containing the prompt")
Parser.add_argument("-Host", default="http://10.1.65.4:11434", type=str, help="HTTP URL to ollama instance")
Parser.add_argument("-WriterModel", default="emm9625/miqu-1-103b:latest", type=str, help="Model to use for writing the base content")
Parser.add_argument("-RevisionModel", default="llama3:70b", type=str, help="Model to use for generating constructive criticism")
Parser.add_argument("-EvalModel", default="llama3:70b", type=str, help="Model to use for evaluating the rating out of 100")
Parser.add_argument("-InfoModel", default="llama3:70b", type=str, help="Model to use when generating summary/info at the end")
Parser.add_argument("-ScrubModel", default="llama3:70b", type=str, help="Model to use when scrubbing the story at the end")
Parser.add_argument("-Seed", default=12, type=int, help="Used to seed models.")
# Parser.add_argument("-OutlineQuality", default=85, type=int, help="Rating out of 100 that the outline must be given by the EvalModel before proceeding to be written")
Parser.add_argument("-OutlineMinRevisions", default=0, type=int, help="Number of minimum revisions that the outline must be given prior to proceeding")
Parser.add_argument("-OutlineMaxRevisions", default=3, type=int, help="Max number of revisions that the outline may have")
# Parser.add_argument("-ChapterQuality", default=85, type=int, help="Rating out of 100 that the chapter must be given by the EvalModel before proceeding to be written")
Parser.add_argument("-ChapterMinRevisions", default=0, type=int, help="Number of minimum revisions that the chapter must be given prior to proceeding")
Parser.add_argument("-ChapterMaxRevisions", default=3, type=int, help="Max number of revisions that the chapter may have")
Parser.add_argument("-NoChapterRevision", action="store_true", help="Disables Chapter Revisions")
Parser.add_argument("-NoScrubChapters", action="store_true", help="Disables a final pass over the story to remove prompt leftovers/outline tidbits.")
Parser.add_argument("-NoExpandOutline", action="store_true", help="Disables the system from expanding the outline for the story chapter by chapter prior to writing the story's chapter content.")
Parser.add_argument("-EnableFinalEditPass", action="store_true", help="Enable a final edit pass of the whole story prior to scrubbing.")
Args = Parser.parse_args()


# Measure Generation Time
StartTime = time.time()


# Setup Config
Writer.Config.SEED = Args.Seed

Writer.Config.WRITER_MODEL = Args.WriterModel
Writer.Config.EVAL_MODEL = Args.EvalModel
Writer.Config.REVISION_MODEL = Args.RevisionModel
Writer.Config.INFO_MODEL = Args.InfoModel
Writer.Config.SCRUB_MODEL = Args.ScrubModel

# Writer.Config.OUTLINE_QUALITY = Args.OutlineQuality
Writer.Config.OUTLINE_MIN_REVISIONS = Args.OutlineMinRevisions
Writer.Config.OUTLINE_MAX_REVISIONS = Args.OutlineMaxRevisions

# Writer.Config.CHAPTER_QUALITY = Args.ChapterQuality
Writer.Config.CHAPTER_MIN_REVISIONS = Args.ChapterMinRevisions
Writer.Config.CHAPTER_MAX_REVISIONS = Args.ChapterMaxRevisions
Writer.Config.CHAPTER_NO_REVISIONS = Args.NoChapterRevision

Writer.Config.SCRUB_NO_SCRUB = Args.NoScrubChapters
Writer.Config.NO_EXPAND_OUTLINE = Args.NoExpandOutline
Writer.Config.ENABLE_FINAL_EDIT_PASS = Args.EnableFinalEditPass



# Initialize Client
Writer.PrintUtils.PrintBanner("Created OLLAMA Client", "red")
Client = Writer.OllamaInterface.InitClient(Args.Host)

# Generate the Outline
Prompt:str = ""
with open(Args.Prompt, "r") as f:
    Prompt = f.read()
Outline = Writer.OutlineGenerator.GenerateOutline(Client, Prompt, Writer.Config.OUTLINE_QUALITY)
BasePrompt = Prompt


## Setup Base Prompt For Chapter-Outline Generation
Prompt = f"""
Please write an engaging and well-paced fictional novel based on the following outline:

---
{Outline}
---

Remember to keep the following criteria in mind:
    - Pacing: Is the story rushing over certain plot points and excessively focusing on others?
    - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?
    - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
    - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?

"""
Messages = [Writer.OllamaInterface.BuildUserQuery(Prompt)]


# Detect the number of chapters
Writer.PrintUtils.PrintBanner("Detecting Chapters", "yellow")
NumChapters:int = Writer.ChapterDetector.LLMCountChapters(Client, Writer.OllamaInterface.GetLastMessageText(Messages))
Writer.PrintUtils.PrintBanner(f"Found {NumChapters} Chapter(s)", "yellow")


# Write Chapter Outlines
ChapterOutlines:list = []
if (not Writer.Config.NO_EXPAND_OUTLINE):
    for Chapter in range(1, NumChapters + 1):
        ChapterOutline, Messages = Writer.OutlineGenerator.GeneratePerChapterOutline(Client, Chapter, Messages)
        ChapterOutlines.append(ChapterOutline)

# Create MegaOutline
DetailedOutline:str = ""
for Chapter in ChapterOutlines:
    DetailedOutline += Chapter
MegaOutline:str = f"""

# Base Outline
{Outline}

# Detailed Outline
{DetailedOutline}

"""

# Setup Base Prompt For Per-Chapter Generation
Prompt = f"""
Please write an engaging and well-paced fictional novel based on the following outline:

---
{MegaOutline}
---

Remember to keep the following criteria in mind:
    - Pacing: Is the story rushing over certain plot points and excessively focusing on others?
    - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?
    - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
    - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?

"""
Messages = [Writer.OllamaInterface.BuildUserQuery(Prompt)]


# Write the chapters
Writer.PrintUtils.PrintBanner("Starting Chapter Writing", "yellow")
Chapters = []
for i in range(1, NumChapters + 1):

    Chapter = Writer.OutlineGenerator.GenerateChapter(Client, i, NumChapters, Outline, Messages, Writer.Config.OUTLINE_QUALITY)

    Messages.append(Writer.OllamaInterface.BuildUserQuery(Chapter))
    Chapters.append(Chapter)
    ChapterWordCount = Writer.Statistics.GetWordCount(Chapter)
    Writer.PrintUtils.PrintBanner(f"Chapter Word Count: {ChapterWordCount}", "blue")


# Now edit the whole thing together
StoryBodyText:str = ""
if Writer.Config.ENABLE_FINAL_EDIT_PASS:
    NewChapters = Writer.NovelEditor.EditNovel(Client, Chapters, Outline, NumChapters)
NewChapters = Chapters

# Now scrub it (if enabled)
if (not Writer.Config.SCRUB_NO_SCRUB):
    NewChapters = Writer.Scrubber.ScrubNovel(Client, NewChapters, NumChapters)
else:
    Writer.PrintUtils.PrintBanner(f"Skipping Scrubbing Due To Config", "yellow")


# Compile The Story
for Chapter in NewChapters:
    StoryBodyText += Chapter + "\n\n\n"



# Now Generate Info
Info = Writer.StoryInfo.GetStoryInfo(Client, Messages)
Title = Info['Title']
Summary = Info['Summary']
Tags = Info['Tags']

print("---------------------------------------------")
print(f"Story Title: {Title}")
print(f"Summary: {Summary}")
print(f"Tags: {Tags}")
print("---------------------------------------------")

ElapsedTime = time.time() - StartTime


# Calculate Total Words
TotalWords:int = Writer.Statistics.GetWordCount(StoryBodyText)
Writer.PrintUtils.PrintBanner(f"Story Total Word Count: {TotalWords}", "blue")

StatsString:str = "Work Statistics:  \n"
StatsString += " - Total Words: " + str(TotalWords) + "  \n"
StatsString += f" - Title: {Title}  \n"
StatsString += f" - Summary: {Summary}  \n"
StatsString += f" - Tags: {Tags}  \n"
StatsString += f" - Generation Start Date: {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}  \n"
StatsString += f" - Generation Total Time: {ElapsedTime}s  \n"
StatsString += f" - Generation Average WPM: {60 * (TotalWords/ElapsedTime)}  \n"

StatsString += "\n\nUser Settings:  \n"
StatsString += f" - Base Prompt: {BasePrompt}  \n"

StatsString += "\n\nGeneration Settings:  \n"
StatsString += f" - Generator: Datacrystals_StoryGenerator_2024-05-14  \n"
StatsString += f" - Writer Model: {Writer.Config.WRITER_MODEL}  \n"
StatsString += f" - Revision Model: {Writer.Config.REVISION_MODEL}  \n"
StatsString += f" - Eval Model: {Writer.Config.EVAL_MODEL}  \n"
StatsString += f" - Info Model: {Writer.Config.INFO_MODEL}  \n"
StatsString += f" - Scrub Model: {Writer.Config.SCRUB_MODEL}  \n"
StatsString += f" - Seed: {Writer.Config.SEED}  \n"
StatsString += f" - Outline Quality: {Writer.Config.OUTLINE_QUALITY}  \n"
StatsString += f" - Outline Min Revisions: {Writer.Config.OUTLINE_MIN_REVISIONS}  \n"
StatsString += f" - Outline Max Revisions: {Writer.Config.OUTLINE_MAX_REVISIONS}  \n"
StatsString += f" - Chapter Quality: {Writer.Config.CHAPTER_QUALITY}  \n"
StatsString += f" - Chapter Min Revisions: {Writer.Config.CHAPTER_MIN_REVISIONS}  \n"
StatsString += f" - Chapter Max Revisions: {Writer.Config.CHAPTER_MAX_REVISIONS}  \n"
StatsString += f" - Chapter Disable Revisions: {Writer.Config.CHAPTER_NO_REVISIONS}  \n"
StatsString += f" - Disable Scrubbing: {Writer.Config.SCRUB_NO_SCRUB}  \n"



# Save The Story To Disk
Writer.PrintUtils.PrintBanner("Saving Story To Disk", "yellow")
FName = f"Stories/Story_{Title.replace(' ', '_')}.md"
with open(FName, "w") as F:
    Out = f"""
{StatsString}

---

Note: An outline of the story is available at the bottom of this document.
Please scroll to the bottom if you wish to read that.

---
# {Title}

{StoryBodyText}


---
# Outline

{Outline}
"""
    F.write(Out)
