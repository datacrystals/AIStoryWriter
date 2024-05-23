import Writer.LLMEditor
import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.Config


def ReviseOutline(_Client, _Outline, _Feedback, _History:list = []):

    RevisionPrompt:str = f"""
Please revise the following outline:
---
{_Outline}
---

Based on the following feedback:
---
{_Feedback}
---

Remember to expand upon your outline and add content to make it as best as it can be!


As you write, keep the following in mind:
    - What is the conflict?
    - Who are the characters (at least two characters)?
    - What do the characters mean to each other?
    - Where are we located?
    - What are the stakes (is it high, is it low, what is at stake here)?
    - What is the goal or solution to the conflict?

    """

    Writer.PrintUtils.PrintBanner("Revising Outline", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(RevisionPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.WRITER_MODEL)
    SummaryText:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner("Done Revising Outline", "green")

    return SummaryText, Messages


def GeneratePerChapterOutline(_Client, _Chapter, _History:list = []):

    RevisionPrompt:str = f"""
Please generate an outline for chapter {_Chapter} from the previous outline.

As you write, keep the following in mind:
    - What is the conflict?
    - Who are the characters (at least two characters)?
    - What do the characters mean to each other?
    - Where are we located?
    - What are the stakes (is it high, is it low, what is at stake here)?
    - What is the goal or solution to the conflict?

Remember to follow the provided outline when creating your chapter.

    """

    Writer.PrintUtils.PrintBanner("Generating Outline For Chapter " + str(_Chapter), "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(RevisionPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.WRITER_MODEL)
    SummaryText:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner("Done Generating Outline For Chapter " + str(_Chapter), "green")

    return SummaryText, Messages



def GenerateOutline(_Client, _OutlinePrompt, _QualityThreshold:int = 85):

    Prompt:str = f"""
Please write a markdown formatted outline based on the following prompt:
---
{_OutlinePrompt}
---
As you write, remember to ask yourself the following questions:
    - What is the conflict?
    - Who are the characters (at least two characters)?
    - What do the characters mean to each other?
    - Where are we located?
    - What are the stakes (is it high, is it low, what is at stake here)?
    - What is the goal or solution to the conflict?

    """

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
    Iterations:int = 0
    while True:
        Iterations += 1
        Feedback, FeedbackHistory = Writer.LLMEditor.GetFeedbackOnOutline(_Client, Outline, FeedbackHistory)
        Rating, FeedbackHistory = Writer.LLMEditor.GetOutlineRating(_Client, Outline, FeedbackHistory)
        # Rating has been changed from a 0-100 int, to does it meet the standards (yes/no)?

        if (Iterations > Writer.Config.OUTLINE_MAX_REVISIONS):
            break
        if ((Iterations > Writer.Config.OUTLINE_MIN_REVISIONS) and (Rating == True)):
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
Please write chapter {_ChapterNum} based on the following outline.

---
{_Outline}
---

As a reminder to keep the following criteria in mind:
    - Pacing: Is the story rushing over certain plot points and excessively focusing on others?
    - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?
    - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
    - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?

Remember - you are the author of this story so don't just answer the above questions, ask them to yourself as you write the story itself.    

"""

    # Generate Initial Chapter
    Writer.PrintUtils.PrintBanner(f"Generating Initial Chapter {_ChapterNum}/{_TotalChapters}", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))

    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.WRITER_MODEL)
    Chapter:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner(f"Done Generating Initial Chapter {_ChapterNum}/{_TotalChapters}", "green")

    if (Writer.Config.CHAPTER_NO_REVISIONS):
        Writer.PrintUtils.PrintBanner(f"Chapter Revision Disabled In Config, Exiting Now", "green")
        return Chapter


    Writer.PrintUtils.PrintBanner(f"Entering Feedback/Revision Loop For Chapter {_ChapterNum}/{_TotalChapters}", "yellow")
    FeedbackHistory = []
    WritingHistory = Messages
    Rating:int = 0
    Iterations:int = 0
    while True:
        Iterations += 1
        Feedback, FeedbackHistory = Writer.LLMEditor.GetFeedbackOnChapter(_Client, Chapter, _Outline, FeedbackHistory)
        Rating, FeedbackHistory = Writer.LLMEditor.GetChapterRating(_Client, Chapter, FeedbackHistory)

        if (Iterations > Writer.Config.CHAPTER_MAX_REVISIONS):
            break
        if ((Iterations > Writer.Config.CHAPTER_MIN_REVISIONS) and (Rating == True)):
            break
        Chapter, WritingHistory = ReviseChapter(_Client, Chapter, Feedback, WritingHistory)

    Writer.PrintUtils.PrintBanner(f"Quality Standard Met, Exiting Feedback/Revision Loop For Chapter {_ChapterNum}/{_TotalChapters}", "yellow")

    return Chapter
