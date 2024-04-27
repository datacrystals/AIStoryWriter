import Writer.Config
import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.ChapterDetector
import Writer.Statistics
import Writer.OutlineGenerator
import Writer.StoryInfo
import Writer.NovelEditor

import argparse

Parser = argparse.ArgumentParser()
Parser.add_argument("Prompt", help="Path to file containing the prompt")
Parser.add_argument("Host", default="http://10.1.65.4:11434", help="HTTP URL to ollama instance")
Args = Parser.parse_args()

# Initialize Client
Writer.PrintUtils.PrintBanner("Created OLLAMA Client", "red")
Client = Writer.OllamaInterface.InitClient(Args.Host)

# Generate the Outline
Prompt:str = ""
with open(Args.Prompt, "r") as f:
    Prompt = f.read()
Outline = Writer.OutlineGenerator.GenerateOutline(Client, Prompt, Writer.Config.OUTLINE_QUALITY)


Prompt = "Here is an outline that you will use to build your award winning novel from. Remember to spell the character's names correctly.\n\n"
Prompt += Outline
Messages = [Writer.OllamaInterface.BuildUserQuery(Prompt)]


# Detect the number of chapters
Writer.PrintUtils.PrintBanner("Detecting Chapters", "yellow")
NumChapters:int = Writer.ChapterDetector.CountChapters(Writer.OllamaInterface.GetLastMessageText(Messages))
Writer.PrintUtils.PrintBanner(f"Found {NumChapters} Chapter(s)", "yellow")


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
NewChapters = Writer.NovelEditor.EditNovel(Client, Chapters, Outline, NumChapters)
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


# Calculate Total Words
TotalWords:int = Writer.Statistics.GetWordCount(StoryBodyText)
Writer.PrintUtils.PrintBanner(f"Story Total Word Count: {TotalWords}", "blue")

StatsString:str = "Work Statistics:\n"
StatsString += " - Total Words: " + str(TotalWords) + "\n"
StatsString += f" - Title: {Title}\n"
StatsString += f" - Summary: {Summary}\n"
StatsString += f" - Tags: {Tags}\n"

StatsString += "\n\nUser Settings:\n"
StatsString += f" - Base Prompt: {Prompt}\n"


# Save The Story To Disk
Writer.PrintUtils.PrintBanner("Saving Story To Disk", "yellow")
FName = f"Stories/Story_{Title.replace(' ', '_')}.md"
with open(FName, "w") as F:
    Out = StatsString + "\n\n\n==============\n\n\n"
    Out += Outline + "\n\n\n==============\n\n\n"
    Out += StoryBodyText
    F.write(Out)
