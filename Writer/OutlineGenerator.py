import Writer.LLMEditor
import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.Config


def ReviseOutline(_Client, _Outline, _Feedback, _History:list = []):

    RevisionPrompt = "Please revise the following outline:\n\n"
    RevisionPrompt += _Outline
    RevisionPrompt += "\n\nBased on the following feedback:\n\n"
    RevisionPrompt += _Feedback
    RevisionPrompt += "\n\nRemember to expand upon your outline and add content to make it as best as it can be!"

    Writer.PrintUtils.PrintBanner("Revising Outline", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(RevisionPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.WRITER_MODEL)
    SummaryText:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner("Done Revising Outline", "green")

    return SummaryText, Messages

def GenerateOutline(_Client, _OutlinePrompt, _QualityThreshold:int = 85):

    Prompt = "Please write a markdown formatted outline based on the following prompt:\n\n"
    Prompt += _OutlinePrompt
    Prompt += "\nRemember to use actual numbers for chapter numbers, e.g. 1 not one."

    # Generate Initial Outline
    Writer.PrintUtils.PrintBanner("Generating Initial Outline", "green")
    Messages = [Writer.OllamaInterface.BuildUserQuery(Prompt)]
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.WRITER_MODEL)
    Outline:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner("Done Generating Initial Outline", "green")

    
    Writer.PrintUtils.PrintBanner("Entering Feedback/Revision Loop", "yellow")
    FeedbackHistory = []
    WritingHistory = Messages
    Rating:int = 0
    while True:
        Feedback, FeedbackHistory = Writer.LLMEditor.GetFeedbackOnOutline(_Client, Outline, FeedbackHistory)
        Rating, FeedbackHistory = Writer.LLMEditor.GetOutlineRating(_Client, Outline, FeedbackHistory)

        if (Rating >= _QualityThreshold):
            break

        Outline, WritingHistory = ReviseOutline(_Client, Outline, Feedback, WritingHistory)

    Writer.PrintUtils.PrintBanner("Quality Standard Met, Exiting Feedback/Revision Loop", "yellow")

    return Outline

    


def ReviseChapter(_Client, _Chapter, _Feedback, _History:list = []):

    RevisionPrompt = f"""
Please revise the following chapter:
{_Chapter}
Based on the following feedback:
{_Feedback}
"""

    Writer.PrintUtils.PrintBanner("Revising Chapter", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(RevisionPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.WRITER_MODEL)
    SummaryText:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner("Done Revising Chapter", "green")

    return SummaryText, Messages



def GenerateChapter(_Client, _ChapterNum:int, _TotalChapters:int, _Outline:str, _History:list = [], _QualityThreshold:int = 85):

    Prompt = f"""
Please write chapter {_ChapterNum} based on the outline.

Only write this chapter (we will get to the rest later), and make it as long and juicy as possible.

As a reminder, here is the outline:
---
{_Outline}
---
"""

    # Generate Initial Chapter
    Writer.PrintUtils.PrintBanner(f"Generating Initial Chapter {_ChapterNum}/{_TotalChapters}", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))

    # print(f"\n\n\n\n\n\n\n\n\n\n---------------------------")
    # Writer.PrintUtils.PrintMessageHistory(Messages)
    # print(f"---------------------------\n\n\n\n\n\n\n\n\n\n\n")

    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.WRITER_MODEL)
    Chapter:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner(f"Done Generating Initial Chapter {_ChapterNum}/{_TotalChapters}", "green")


    Writer.PrintUtils.PrintBanner(f"Entering Feedback/Revision Loop For Chapter {_ChapterNum}/{_TotalChapters}", "yellow")
    FeedbackHistory = []
    WritingHistory = Messages
    Rating:int = 0
    while True:
        Feedback, FeedbackHistory = Writer.LLMEditor.GetFeedbackOnChapter(_Client, Chapter, _Outline, FeedbackHistory)
        Rating, FeedbackHistory = Writer.LLMEditor.GetChapterRating(_Client, Chapter, FeedbackHistory)

        if (Rating >= _QualityThreshold):
            break
        Chapter, WritingHistory = ReviseChapter(_Client, Chapter, Feedback, WritingHistory)

    Writer.PrintUtils.PrintBanner(f"Quality Standard Met, Exiting Feedback/Revision Loop For Chapter {_ChapterNum}/{_TotalChapters}", "yellow")

    return Chapter
