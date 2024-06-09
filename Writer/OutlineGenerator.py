import Writer.LLMEditor
import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.Config



def GenerateOutline(_Client, _OutlinePrompt, _QualityThreshold:int = 85):

    Prompt:str = f"""
Please write a markdown formatted outline based on the following prompt:

```
{_OutlinePrompt}
```

As you write, remember to ask yourself the following questions:
    - What is the conflict?
    - Who are the characters (at least two characters)?
    - What do the characters mean to each other?
    - Where are we located?
    - What are the stakes (is it high, is it low, what is at stake here)?
    - What is the goal or solution to the conflict?

Don't answer these questions directly, instead make your outline implicitly answer them. (Show, don't tell)

Please keep your outline clear as to what content is in what chapter.
Make sure to add lots of detail as you write.

Again, remember - you're writing an outline for the story.
    
    """

    # Generate Initial Outline
    Writer.PrintUtils.PrintBanner("Generating Initial Outline", "green")
    Messages = [Writer.OllamaInterface.BuildUserQuery(Prompt)]
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL)
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


def ReviseOutline(_Client, _Outline, _Feedback, _History:list = []):

    RevisionPrompt:str = f"""
Please revise the following outline:
```
{_Outline}
```

Based on the following feedback:
```
{_Feedback}
```

Remember to expand upon your outline and add content to make it as best as it can be!


As you write, keep the following in mind:
    - What is the conflict?
    - Who are the characters (at least two characters)?
    - What do the characters mean to each other?
    - Where are we located?
    - What are the stakes (is it high, is it low, what is at stake here)?
    - What is the goal or solution to the conflict?


Please keep your outline clear as to what content is in what chapter.
Make sure to add lots of detail as you write.

Don't answer these questions directly, instead make your writing implicitly answer them. (Show, don't tell)

    """

    Writer.PrintUtils.PrintBanner("Revising Outline", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(RevisionPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL)
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

Remember to follow the provided outline when creating your chapter outline.

Don't answer these questions directly, instead make your outline implicitly answer them. (Show, don't tell)

Again, don't write the chapter itself, just create a detailed outline of the chapter.  

Make sure your chapter has a markdown-formatted name!

    """

    Writer.PrintUtils.PrintBanner("Generating Outline For Chapter " + str(_Chapter), "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(RevisionPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL)
    SummaryText:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner("Done Generating Outline For Chapter " + str(_Chapter), "green")

    return SummaryText, Messages


