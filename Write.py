import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.ChapterDetector



# Initialize Client
Writer.PrintUtils.PrintBanner("Created OLLAMA Client", "red")
Client = Writer.OllamaInterface.InitClient("http://10.1.65.4:11434")
Writer.PrintUtils.PrintBanner("Spinning Up Model For first Inference")

StartingPrompt:str = '''
Please outline a 5k word story about Kaveh from genshin. Make a markdown formatted outline, with a numbered list for each chapter and bullet points for each part of what it contains.
'''

Messages = [Writer.OllamaInterface.BuildUserQuery(StartingPrompt)]
Messages = Writer.OllamaInterface.ChatAndStreamResponse(Client, Messages)
SummaryText:str = Writer.OllamaInterface.GetLastMessageText(Messages)

Writer.PrintUtils.PrintBanner("Detecting Chapters", "yellow")
NumChapters:int = Writer.ChapterDetector.CountChapters(Writer.OllamaInterface.GetLastMessageText(Messages))
Writer.PrintUtils.PrintBanner(f"Found {NumChapters} Chapter(s)", "yellow")

Writer.PrintUtils.PrintBanner("Starting Chapter Writing", "yellow")
StoryBodyText:str = ""
for Chapter in range(NumChapters):

    PromptStr:str = f"Please write Chapter {Chapter + 1}"
    Writer.PrintUtils.PrintBanner(f"Prompting: {PromptStr}", "green")

    Messages.append(Writer.OllamaInterface.BuildUserQuery(PromptStr))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(Client, Messages)

    StoryBodyText += Writer.OllamaInterface.GetLastMessageText(Messages) + "\n\n\n"



# Calculate Total Words
TotalWords:int = len(StoryBodyText.split())
Writer.PrintUtils.PrintBanner(f"Story Total Word Count: {TotalWords}", "blue")

StatsString:str = "Work Statistics"
StatsString += "Total Words: " + str(TotalWords)


Writer.PrintUtils.PrintBanner("Saving Story To Disk", "yellow")
with open("Story.txt", "w") as F:
    Out = StatsString + "\n\n\n==============\n\n\n"
    Out += SummaryText + "\n\n\n==============\n\n\n"
    Out += StoryBodyText
    F.write(Out)
