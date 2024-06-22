#!/bin/python3

import argparse
import time
import datetime
import os

import Writer.Config
import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.ChapterDetector
import Writer.Scrubber
import Writer.Statistics
import Writer.OutlineGenerator
import Writer.ChapterGenerator
import Writer.StoryInfo
import Writer.NovelEditor
import Writer.Translator


# Setup Argparser
Parser = argparse.ArgumentParser()
Parser.add_argument("-Prompt", help="Path to file containing the prompt")
Parser.add_argument("-Output", default="", type=str, help="Optional file output path, if none is speciifed, we will autogenerate a file name based on the story title")
Parser.add_argument("-Host", default="http://10.1.65.4:11434", type=str, help="HTTP URL to ollama instance")
Parser.add_argument("-InitialOutlineModel", default="llama3:70b", type=str, help="Model to use for writing the base outline content")
Parser.add_argument("-ChapterOutlineModel", default="llama3:70b", type=str, help="Model to use for writing the per-chapter outline content")
Parser.add_argument("-ChapterS1Model", default="llama3:70b", type=str, help="Model to use for writing the chapter (stage 1: plot)")
Parser.add_argument("-ChapterS2Model", default="llama3:70b", type=str, help="Model to use for writing the chapter (stage 2: character development)")
Parser.add_argument("-ChapterS3Model", default="llama3:70b", type=str, help="Model to use for writing the chapter (stage 3: dialogue)")
Parser.add_argument("-ChapterS4Model", default="llama3:70b", type=str, help="Model to use for writing the chapter (stage 4: final correction pass)")
Parser.add_argument("-ChapterRevisionModel", default="llama3:70b", type=str, help="Model to use for revising the chapter until it meets criteria")
Parser.add_argument("-RevisionModel", default="llama3:70b", type=str, help="Model to use for generating constructive criticism")
Parser.add_argument("-EvalModel", default="llama3:70b", type=str, help="Model to use for evaluating the rating out of 100")
Parser.add_argument("-InfoModel", default="llama3:70b", type=str, help="Model to use when generating summary/info at the end")
Parser.add_argument("-ScrubModel", default="llama3:70b", type=str, help="Model to use when scrubbing the story at the end")
Parser.add_argument("-CheckerModel", default="llama3:70b", type=str, help="Model to use when checking if the LLM cheated or not")
Parser.add_argument("-TranslatorModel", default="llama3:70b", type=str, help="Model to use if translation of the story is enabled")
Parser.add_argument("-Translate", default="", type=str, help="Specify a language to translate the story to - will not translate by default. Ex: 'French'")
Parser.add_argument("-TranslatePrompt", default="", type=str, help="Specify a language to translate your input prompt to. Ex: 'French'")
Parser.add_argument("-Seed", default=12, type=int, help="Used to seed models.")
Parser.add_argument("-OutlineMinRevisions", default=0, type=int, help="Number of minimum revisions that the outline must be given prior to proceeding")
Parser.add_argument("-OutlineMaxRevisions", default=3, type=int, help="Max number of revisions that the outline may have")
Parser.add_argument("-ChapterMinRevisions", default=0, type=int, help="Number of minimum revisions that the chapter must be given prior to proceeding")
Parser.add_argument("-ChapterMaxRevisions", default=3, type=int, help="Max number of revisions that the chapter may have")
Parser.add_argument("-NoChapterRevision", action="store_true", help="Disables Chapter Revisions")
Parser.add_argument("-NoScrubChapters", action="store_true", help="Disables a final pass over the story to remove prompt leftovers/outline tidbits")
Parser.add_argument("-ExpandOutline", action="store_true", help="Disables the system from expanding the outline for the story chapter by chapter prior to writing the story's chapter content")
Parser.add_argument("-EnableFinalEditPass", action="store_true", help="Enable a final edit pass of the whole story prior to scrubbing")
Parser.add_argument("-Debug", action="store_true", help="Print system prompts to stdout during generation")
Args = Parser.parse_args()


# Measure Generation Time
StartTime = time.time()


# Setup Config
Writer.Config.SEED = Args.Seed

Writer.Config.INITIAL_OUTLINE_WRITER_MODEL = Args.InitialOutlineModel
Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL = Args.ChapterOutlineModel
Writer.Config.CHAPTER_STAGE1_WRITER_MODEL = Args.ChapterS1Model
Writer.Config.CHAPTER_STAGE2_WRITER_MODEL = Args.ChapterS2Model
Writer.Config.CHAPTER_STAGE3_WRITER_MODEL = Args.ChapterS3Model
Writer.Config.CHAPTER_STAGE4_WRITER_MODEL = Args.ChapterS4Model
Writer.Config.CHAPTER_REVISION_WRITER_MODEL = Args.ChapterRevisionModel
Writer.Config.EVAL_MODEL = Args.EvalModel
Writer.Config.REVISION_MODEL = Args.RevisionModel
Writer.Config.INFO_MODEL = Args.InfoModel
Writer.Config.SCRUB_MODEL = Args.ScrubModel
Writer.Config.CHECKER_MODEL = Args.CheckerModel
Writer.Config.TRANSLATOR_MODEL = Args.TranslatorModel

Writer.Config.TRANSLATE_LANGUAGE = Args.Translate
Writer.Config.TRANSLATE_PROMPT_LANGUAGE = Args.TranslatePrompt

Writer.Config.OUTLINE_MIN_REVISIONS = Args.OutlineMinRevisions
Writer.Config.OUTLINE_MAX_REVISIONS = Args.OutlineMaxRevisions

Writer.Config.CHAPTER_MIN_REVISIONS = Args.ChapterMinRevisions
Writer.Config.CHAPTER_MAX_REVISIONS = Args.ChapterMaxRevisions
Writer.Config.CHAPTER_NO_REVISIONS = Args.NoChapterRevision

Writer.Config.SCRUB_NO_SCRUB = Args.NoScrubChapters
Writer.Config.EXPAND_OUTLINE = Args.ExpandOutline
Writer.Config.ENABLE_FINAL_EDIT_PASS = Args.EnableFinalEditPass

Writer.Config.OPTIONAL_OUTPUT_NAME = Args.Output
Writer.Config.DEBUG = Args.Debug


# Setup Logger
SysLogger = Writer.PrintUtils.Logger()

# Initialize Client
SysLogger.Log("Created OLLAMA Client", 5)
Client = Writer.OllamaInterface.InitClient(Args.Host)

# Load User Prompt
Prompt:str = ""
with open(Args.Prompt, "r") as f:
    Prompt = f.read()


# If user wants their prompt translated, do so
if (Writer.Config.TRANSLATE_PROMPT_LANGUAGE != ""):
    Prompt = Writer.Translator.TranslatePrompt(Client, SysLogger, Prompt, Writer.Config.TRANSLATE_PROMPT_LANGUAGE)


# Generate the Outline
Outline = Writer.OutlineGenerator.GenerateOutline(Client, SysLogger, Prompt, Writer.Config.OUTLINE_QUALITY)
BasePrompt = Prompt


# Detect the number of chapters
SysLogger.Log("Detecting Chapters", 5)
Messages = [Writer.OllamaInterface.BuildUserQuery(Outline)]
NumChapters:int = Writer.ChapterDetector.LLMCountChapters(Client, SysLogger, Writer.OllamaInterface.GetLastMessageText(Messages))
SysLogger.Log(f"Found {NumChapters} Chapter(s)", 5)


## Write Per-Chapter Outline
Prompt = f"""
Please help me expand upon the following outline, chapter by chapter.

```
{Outline}
```
    
"""
Messages = [Writer.OllamaInterface.BuildUserQuery(Prompt)]
ChapterOutlines:list = []
if (Writer.Config.EXPAND_OUTLINE):
    for Chapter in range(1, NumChapters + 1):
        ChapterOutline, Messages = Writer.OutlineGenerator.GeneratePerChapterOutline(Client, SysLogger, Chapter, Messages)
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
UsedOutline:str = Outline
if (Writer.Config.EXPAND_OUTLINE):
    UsedOutline = MegaOutline


# Write the chapters
SysLogger.Log("Starting Chapter Writing", 5)
Chapters = []
for i in range(1, NumChapters + 1):

    Chapter = Writer.ChapterGenerator.GenerateChapter(Client, SysLogger, i, NumChapters, Outline, Chapters, Writer.Config.OUTLINE_QUALITY)

    Chapter = f"### Chapter {i}\n\n{Chapter}"
    Chapters.append(Chapter)
    ChapterWordCount = Writer.Statistics.GetWordCount(Chapter)
    SysLogger.Log(f"Chapter Word Count: {ChapterWordCount}", 2)


# Now edit the whole thing together
StoryBodyText:str = ""
if Writer.Config.ENABLE_FINAL_EDIT_PASS:
    NewChapters = Writer.NovelEditor.EditNovel(Client, SysLogger, Chapters, Outline, NumChapters)
NewChapters = Chapters

# Now scrub it (if enabled)
if (not Writer.Config.SCRUB_NO_SCRUB):
    NewChapters = Writer.Scrubber.ScrubNovel(Client, SysLogger, NewChapters, NumChapters)
else:
    SysLogger.Log(f"Skipping Scrubbing Due To Config", 4)


# If enabled, translate the novel
if (Writer.Config.TRANSLATE_LANGUAGE != ""):
    NewChapters = Writer.Translator.TranslateNovel(Client, SysLogger, NewChapters, NumChapters, Writer.Config.TRANSLATE_LANGUAGE)
else:
    SysLogger.Log(f"No Novel Translation Requested, Skipping Translation Step", 4)



# Compile The Story
for Chapter in NewChapters:
    StoryBodyText += Chapter + "\n\n\n"



# Now Generate Info
Messages = []
Messages.append(Writer.OllamaInterface.BuildUserQuery(Outline))
Info = Writer.StoryInfo.GetStoryInfo(Client, SysLogger, Messages)
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
SysLogger.Log(f"Story Total Word Count: {TotalWords}", 4)

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
StatsString += f" - Generator: AIStoryGenerator_2024-06-21  \n"
StatsString += f" - Base Outline Writer Model: {Writer.Config.INITIAL_OUTLINE_WRITER_MODEL}  \n"
StatsString += f" - Chapter Outline Writer Model: {Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL}  \n"
StatsString += f" - Chapter Writer (Stage 1: Plot) Model: {Writer.Config.CHAPTER_STAGE1_WRITER_MODEL}  \n"
StatsString += f" - Chapter Writer (Stage 2: Char Development) Model: {Writer.Config.CHAPTER_STAGE2_WRITER_MODEL}  \n"
StatsString += f" - Chapter Writer (Stage 3: Dialogue) Model: {Writer.Config.CHAPTER_STAGE3_WRITER_MODEL}  \n"
StatsString += f" - Chapter Writer (Stage 4: Final Pass) Model: {Writer.Config.CHAPTER_STAGE4_WRITER_MODEL}  \n"
StatsString += f" - Chapter Writer (Revision) Model: {Writer.Config.CHAPTER_REVISION_WRITER_MODEL}  \n"
StatsString += f" - Revision Model: {Writer.Config.REVISION_MODEL}  \n"
StatsString += f" - Eval Model: {Writer.Config.EVAL_MODEL}  \n"
StatsString += f" - Info Model: {Writer.Config.INFO_MODEL}  \n"
StatsString += f" - Scrub Model: {Writer.Config.SCRUB_MODEL}  \n"
StatsString += f" - Seed: {Writer.Config.SEED}  \n"
# StatsString += f" - Outline Quality: {Writer.Config.OUTLINE_QUALITY}  \n"
StatsString += f" - Outline Min Revisions: {Writer.Config.OUTLINE_MIN_REVISIONS}  \n"
StatsString += f" - Outline Max Revisions: {Writer.Config.OUTLINE_MAX_REVISIONS}  \n"
# StatsString += f" - Chapter Quality: {Writer.Config.CHAPTER_QUALITY}  \n"
StatsString += f" - Chapter Min Revisions: {Writer.Config.CHAPTER_MIN_REVISIONS}  \n"
StatsString += f" - Chapter Max Revisions: {Writer.Config.CHAPTER_MAX_REVISIONS}  \n"
StatsString += f" - Chapter Disable Revisions: {Writer.Config.CHAPTER_NO_REVISIONS}  \n"
StatsString += f" - Disable Scrubbing: {Writer.Config.SCRUB_NO_SCRUB}  \n"



# Save The Story To Disk
SysLogger.Log("Saving Story To Disk", 3)
os.makedirs("Stories", exist_ok=True)
FName = f"Stories/Story_{Title.replace(' ', '_')}.md"
if (Writer.Config.OPTIONAL_OUTPUT_NAME != ""):
    FName = Writer.Config.OPTIONAL_OUTPUT_NAME
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
```
{Outline}
```
"""
    F.write(Out)
