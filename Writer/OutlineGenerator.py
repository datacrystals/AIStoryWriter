import Writer.LLMEditor
import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.Config
import Writer.Outline.StoryElements


# We should probably do outline generation in stages, allowing us to go back and add foreshadowing, etc back to previous segments


def GenerateOutline(_Client, _Logger, _OutlinePrompt, _QualityThreshold:int = 85):

    # Generate Story Elements
    StoryElements:str = Writer.Outline.StoryElements.GenerateStoryElements(_Client, _Logger, _OutlinePrompt)

    # Now, Generate Initial Outline
    Prompt:str = f"""
Please write a markdown formatted outline based on the following prompt:

<PROMPT>
{_OutlinePrompt}
</PROMPT>

<ELEMENTS>
{StoryElements}
</ELEMENTS>

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

Also, include information about the different characters, and how they change over the course of the story.
We want to have rich and complex character development!

Start your response with '# Outline\n## Chapter 1:'.
    """

    _Logger.Log(f"Generating Initial Outline", 4)
    Messages = [Writer.OllamaInterface.BuildUserQuery(Prompt)]
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL)
    Outline:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    _Logger.Log(f"Done Generating Initial Outline", 4)

    
    _Logger.Log(f"Entering Feedback/Revision Loop", 3)
    FeedbackHistory = []
    WritingHistory = Messages
    Rating:int = 0
    Iterations:int = 0
    while True:
        Iterations += 1
        Feedback, FeedbackHistory = Writer.LLMEditor.GetFeedbackOnOutline(_Client, _Logger, Outline, FeedbackHistory)
        Rating, FeedbackHistory = Writer.LLMEditor.GetOutlineRating(_Client, _Logger, Outline, FeedbackHistory)
        # Rating has been changed from a 0-100 int, to does it meet the standards (yes/no)?

        if (Iterations > Writer.Config.OUTLINE_MAX_REVISIONS):
            break
        if ((Iterations > Writer.Config.OUTLINE_MIN_REVISIONS) and (Rating == True)):
            break

        Outline, WritingHistory = ReviseOutline(_Client, _Logger, Outline, Feedback, WritingHistory)

    _Logger.Log(f"Quality Standard Met, Exiting Feedback/Revision Loop", 4)

    
    # Generate Final Outline
    FinalOutline:str = f'''
{StoryElements}

{Outline}
    '''

    return FinalOutline


def ReviseOutline(_Client, _Logger, _Outline, _Feedback, _History:list = []):

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

    _Logger.Log(f"Revising Outline", 2)
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(RevisionPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL)
    SummaryText:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    _Logger.Log(f"Done Revising Outline", 2)

    return SummaryText, Messages


def GeneratePerChapterOutline(_Client, _Logger, _Chapter, _History:list = []):

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
    _Logger.Log("Generating Outline For Chapter " + str(_Chapter), 5)
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(RevisionPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, _Logger, Messages, Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL)
    SummaryText:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    _Logger.Log("Done Generating Outline For Chapter " + str(_Chapter), 5)

    return SummaryText, Messages


