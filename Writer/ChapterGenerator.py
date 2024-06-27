import json

import Writer.LLMEditor
import Writer.PrintUtils
import Writer.Config
import Writer.ChapterGenSummaryCheck


def GenerateChapter(
    Interface,
    _Logger,
    _ChapterNum: int,
    _TotalChapters: int,
    _Outline: str,
    _Chapters: list = [],
    _QualityThreshold: int = 85,
):

    # Some important notes
    # We're going to remind the author model of the previous chapters here, so it knows what has been written before.

    #### Stage 0: Create base language chain
    _Logger.Log(f"Creating Base Langchain For Chapter {_ChapterNum} Generation", 2)
    MesssageHistory: list = []
    MesssageHistory.append(
        Interface.BuildSystemQuery(
            f"You are a great fiction writer, and you're working on a great new story. You're working on a new novel, and you want to produce a quality output. Here is your outline: \n<OUTLINE>\n{_Outline}\n</OUTLINE>"
        )
    )

    ContextHistoryInsert: str = ""

    if len(_Chapters) > 0:

        ChapterSuperlist: str = ""
        for Chapter in _Chapters:
            ChapterSuperlist += f"{Chapter}\n"

        ContextHistoryInsert += f"""
Please help me write my novel.

I'm basing my work on this outline:

<OUTLINE>
{_Outline}
</OUTLINE>

And here is what I've written so far:
<PREVIOUS_CHAPTERS>
{ChapterSuperlist}
</PREVIOUS_CHAPTERS>

"""
    #
    # MesssageHistory.append(Interface.BuildUserQuery(f"""
    # Here is the novel so far.
    # """))
    # MesssageHistory.append(Interface.BuildUserQuery(ChapterSuperlist))
    # MesssageHistory.append(Interface.BuildSystemQuery("Make sure to pay attention to the content that has happened in these previous chapters. It's okay to deviate from the outline a little in order to ensure you continue the same story from previous chapters."))

    # Now, extract the this-chapter-outline segment
    _Logger.Log(f"Creating Chapter Specific Outline", 4)
    ThisChapterOutline: str = ""
    ChapterSegmentMessages = []
    ChapterSegmentMessages.append(
        Interface.BuildSystemQuery(
            f"You are a helpful AI Assistant. Answer the user's prompts to the best of your abilities."
        )
    )
    ChapterSegmentMessages.append(
        Interface.BuildUserQuery(
            f"""
Please help me extract the part of this outline that is just for chapter {_ChapterNum}.

<OUTLINE>
{_Outline}
</OUTLINE>

Do not include anything else in your response except just the content for chapter {_ChapterNum}.
"""
        )
    )
    ChapterSegmentMessages = Interface.ChatAndStreamResponse(
        _Logger,
        ChapterSegmentMessages,
        Writer.Config.CHAPTER_STAGE1_WRITER_MODEL,
    )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
    ThisChapterOutline: str = Interface.GetLastMessageText(ChapterSegmentMessages)
    _Logger.Log(f"Created Chapter Specific Outline", 4)

    # Generate Summary of Last Chapter If Applicable
    FormattedLastChapterSummary: str = ""
    if len(_Chapters) > 0:
        _Logger.Log(f"Creating Summary Of Last Chapter Info", 3)
        ChapterSummaryMessages = []
        ChapterSummaryMessages.append(
            Interface.BuildSystemQuery(
                f"You are a helpful AI Assistant. Answer the user's prompts to the best of your abilities."
            )
        )
        ChapterSummaryMessages.append(
            Interface.BuildUserQuery(
                f"""
I'm writing the next chapter in my novel (chapter {_ChapterNum}), and I have the following written so far.

My outline:
<OUTLINE>
{_Outline}
</OUTLINE>

And what I've written in the last chapter:
<PREVIOUS_CHAPTER>
{_Chapters[-1]}
</PREVIOUS_CHAPTER>

Please create a list of important summary points from the last chapter so that I know what to keep in mind as I write this chapter.
Also make sure to add a summary of the previous chapter, and focus on noting down any important plot points, and the state of the story as the chapter ends.
That way, when I'm writing, I'll know where to pick up again.

Here's some formatting guidelines:

```
Previous Chapter:
    - Plot:
        - Your bullet point summary here with as much detail as needed
    - Setting:
        - some stuff here
    - Characters:
        - character 1
            - info about them, from that chapter
            - if they changed, how so

Things to keep in Mind:
    - something that the previous chapter did to advance the plot, so we incorporate it into the next chapter
    - something else that is important to remember when writing the next chapter
    - another thing
    - etc.
```

Thank you for helping me write my story! Please only include your summary and things to keep in mind, don't write anything else.
    """
            )
        )
        ChapterSummaryMessages = Interface.ChatAndStreamResponse(
            _Logger,
            ChapterSummaryMessages,
            Writer.Config.CHAPTER_STAGE1_WRITER_MODEL,
        )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
        FormattedLastChapterSummary: str = Interface.GetLastMessageText(
            ChapterSummaryMessages
        )
        _Logger.Log(f"Created Summary Of Last Chapter Info", 3)

    DetailedChapterOutline: str = ThisChapterOutline
    if FormattedLastChapterSummary != "":
        DetailedChapterOutline = ThisChapterOutline

    _Logger.Log(f"Done with base langchain setup", 2)

    #### STAGE 1: Create Initial Plot
    Stage1Chapter = ""
    IterCounter: int = 0
    Feedback: str = ""
    while True:
        Prompt = f"""
{ContextHistoryInsert}

Please write the plot for chapter {_ChapterNum} of {_TotalChapters} based on the following chapter outline and any previous chapters.
Pay attention to the previous chapters, and make sure you both continue seamlessly from them, It's imperative that your writing connects well with the previous chapter, and flows into the next (so try to follow the outline)!

Here is my outline for this chapter:
<CHAPTER_OUTLINE>
{ThisChapterOutline}
</CHAPTER_OUTLINE>

{FormattedLastChapterSummary}

As you write your work, please use the following suggestions to help you write chapter {_ChapterNum} (make sure you only write this one):
    - Pacing: 
    - Are you skipping days at a time? Summarizing events? Don't do that, add scenes to detail them.
    - Is the story rushing over certain plot points and excessively focusing on others?
    - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
    - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?

{Feedback}

    """

        # Generate Initial Chapter
        _Logger.Log(
            f"Generating Initial Chapter (Stage 1: Plot) {_ChapterNum}/{_TotalChapters} (Iteration {IterCounter})",
            5,
        )
        Messages = MesssageHistory.copy()
        Messages.append(Interface.BuildUserQuery(Prompt))

        Messages = Interface.ChatAndStreamResponse(
            _Logger,
            Messages,
            Writer.Config.CHAPTER_STAGE1_WRITER_MODEL,
            _SeedOverride=IterCounter + Writer.Config.SEED,
        )
        IterCounter += 1
        Stage1Chapter: str = Interface.GetLastMessageText(Messages)
        _Logger.Log(
            f"Finished Initial Generation For Initial Chapter (Stage 1: Plot)  {_ChapterNum}/{_TotalChapters}",
            5,
        )

        # Check if LLM did the work
        if IterCounter > Writer.Config.CHAPTER_MAX_REVISIONS:
            _Logger.Log(
                "Chapter Summary-Based Revision Seems Stuck - Forcefully Exiting", 7
            )
            break
        Result, Feedback = Writer.ChapterGenSummaryCheck.LLMSummaryCheck(
            Interface, _Logger, DetailedChapterOutline, Stage1Chapter
        )
        if Result:
            _Logger.Log(
                f"Done Generating Initial Chapter (Stage 1: Plot)  {_ChapterNum}/{_TotalChapters}",
                5,
            )
            break

    #### STAGE 2: Add Character Development
    Stage2Chapter = ""
    IterCounter: int = 0
    Feedback: str = ""
    while True:
        Prompt = f"""
{ContextHistoryInsert}


Please write character development for the following chapter {_ChapterNum} of {_TotalChapters} based on the following criteria and any previous chapters.
Pay attention to the previous chapters, and make sure you both continue seamlessly from them, It's imperative that your writing connects well with the previous chapter, and flows into the next (so try to follow the outline)!

Don't take away content, instead expand upon it to make a longer and more detailed output.

For your reference, here is my outline for this chapter:
<CHAPTER_OUTLINE>
{ThisChapterOutline}
</CHAPTER_OUTLINE>

{FormattedLastChapterSummary}

And here is what I have for the current chapter's plot:
<CHAPTER_PLOT>
{Stage1Chapter}
</CHAPTER_PLOT>

As a reminder to keep the following criteria in mind as you expand upon the above work:
    - Characters: Who are the characters in this chapter? What do they mean to each other? What is the situation between them? Is it a conflict? Is there tension? Is there a reason that the characters have been brought together?
    - Development: What are the goals of each character, and do they meet those goals? Do the characters change and exhibit growth? Do the goals of each character change over the story?
    - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?

Don't answer these questions directly, instead make your writing implicitly answer them. (Show, don't tell)

Make sure that your chapter flows into the next and from the previous (if applicable).

Remember, have fun, be creative, and improve the character development of chapter {_ChapterNum} (make sure you only write this one)!

{Feedback}


"""

        # Generate Initial Chapter
        _Logger.Log(
            f"Generating Initial Chapter (Stage 2: Character Development) {_ChapterNum}/{_TotalChapters} (Iteration {IterCounter})",
            5,
        )
        Messages = MesssageHistory.copy()
        Messages.append(Interface.BuildUserQuery(Prompt))

        Messages = Interface.ChatAndStreamResponse(
            _Logger,
            Messages,
            Writer.Config.CHAPTER_STAGE2_WRITER_MODEL,
            _SeedOverride=IterCounter + Writer.Config.SEED,
        )
        IterCounter += 1
        Stage2Chapter: str = Interface.GetLastMessageText(Messages)
        _Logger.Log(
            f"Finished Initial Generation For Initial Chapter (Stage 2: Character Development)  {_ChapterNum}/{_TotalChapters}",
            5,
        )

        # Check if LLM did the work
        if IterCounter > Writer.Config.CHAPTER_MAX_REVISIONS:
            _Logger.Log(
                "Chapter Summary-Based Revision Seems Stuck - Forcefully Exiting", 7
            )
            break
        Result, Feedback = Writer.ChapterGenSummaryCheck.LLMSummaryCheck(
            Interface, _Logger, DetailedChapterOutline, Stage2Chapter
        )
        if Result:
            _Logger.Log(
                f"Done Generating Initial Chapter (Stage 2: Character Development)  {_ChapterNum}/{_TotalChapters}",
                5,
            )
            break

    #### STAGE 3: Add Dialogue
    Stage3Chapter = ""
    IterCounter: int = 0
    Feedback: str = ""
    while True:
        Prompt = f"""
{ContextHistoryInsert}


Please add dialogue the following chapter {_ChapterNum} of {_TotalChapters} based on the following criteria and any previous chapters.
Pay attention to the previous chapters, and make sure you both continue seamlessly from them, It's imperative that your writing connects well with the previous chapter, and flows into the next (so try to follow the outline)!

Don't take away content, instead expand upon it to make a longer and more detailed output.


{FormattedLastChapterSummary}

Here's what I have so far for this chapter:
<CHAPTER_CONTENT>
{Stage2Chapter}
</CHAPTER_CONTENT

As a reminder to keep the following criteria in mind:
    - Dialogue: Does the dialogue make sense? Is it appropriate given the situation? Does the pacing make sense for the scene E.g: (Is it fast-paced because they're running, or slow-paced because they're having a romantic dinner)? 
    - Disruptions: If the flow of dialogue is disrupted, what is the reason for that disruption? Is it a sense of urgency? What is causing the disruption? How does it affect the dialogue moving forwards? 
     - Pacing: 
       - Are you skipping days at a time? Summarizing events? Don't do that, add scenes to detail them.
       - Is the story rushing over certain plot points and excessively focusing on others?
    
Don't answer these questions directly, instead make your writing implicitly answer them. (Show, don't tell)

Make sure that your chapter flows into the next and from the previous (if applicable).

Also, please remove any headings from the outline that may still be present in the chapter.

Remember, have fun, be creative, and add dialogue to chapter {_ChapterNum} (make sure you only write this one)!

{Feedback}


"""

        # Generate Initial Chapter
        _Logger.Log(
            f"Generating Initial Chapter (Stage 3: Dialogue) {_ChapterNum}/{_TotalChapters} (Iteration {IterCounter})",
            5,
        )
        Messages = MesssageHistory.copy()
        Messages.append(Interface.BuildUserQuery(Prompt))

        Messages = Interface.ChatAndStreamResponse(
            _Logger,
            Messages,
            Writer.Config.CHAPTER_STAGE3_WRITER_MODEL,
            _SeedOverride=IterCounter + Writer.Config.SEED,
        )
        IterCounter += 1
        Stage3Chapter: str = Interface.GetLastMessageText(Messages)
        _Logger.Log(
            f"Finished Initial Generation For Initial Chapter (Stage 3: Dialogue)  {_ChapterNum}/{_TotalChapters}",
            5,
        )

        # Check if LLM did the work
        if IterCounter > Writer.Config.CHAPTER_MAX_REVISIONS:
            _Logger.Log(
                "Chapter Summary-Based Revision Seems Stuck - Forcefully Exiting", 7
            )
            break
        Result, Feedback = Writer.ChapterGenSummaryCheck.LLMSummaryCheck(
            Interface, _Logger, DetailedChapterOutline, Stage3Chapter
        )
        if Result:
            _Logger.Log(
                f"Done Generating Initial Chapter (Stage 3: Dialogue)  {_ChapterNum}/{_TotalChapters}",
                5,
            )
            break

    #     #### STAGE 4: Final-Pre-Revision Edit Pass
    #     Prompt = f"""
    # Please provide a final edit the following chapter based on the following criteria and any previous chapters.
    # Do not summarize any previous chapters, make your chapter connect seamlessly with previous ones.

    # Don't take away content, instead expand upon it to make a longer and more detailed output.

    # For your reference, here is the outline:
    # ```
    # {_Outline}
    # ```

    # And here is the chapter to tweak and improve:
    # ```
    # {Stage3Chapter}
    # ```

    # As a reminder to keep the following criteria in mind:
    #     - Pacing:
    #       - Are you skipping days at a time? Summarizing events? Don't do that, add scenes to detail them.
    #       - Is the story rushing over certain plot points and excessively focusing on others?
    #     - Characters
    #     - Flow
    #     - Details: Is the output too flowery?
    #     - Dialogue
    #     - Development: Is there a clear development from scene to scene, chapter to chapter?
    #     - Genre
    #     - Disruptions/conflict

    # Remember to remove any author notes or non-chapter text, as this is the version that will be published.

    # """

    #     # Generate Initial Chapter
    #     _Logger.Log(f"Generating Initial Chapter (Stage 4: Final Pass) {_ChapterNum}/{_TotalChapters}", 5)
    #     Messages = MesssageHistory.copy()
    #     Messages.append(Interface.BuildUserQuery(Prompt))

    #     Messages = Interface.ChatAndStreamResponse(_Logger, Messages, Writer.Config.CHAPTER_STAGE4_WRITER_MODEL)
    #     Chapter:str = Interface.GetLastMessageText(Messages)
    #     _Logger.Log(f"Done Generating Initial Chapter (Stage 4: Final Pass)  {_ChapterNum}/{_TotalChapters}", 5)
    Chapter: str = Stage3Chapter

    #### Stage 5: Revision Cycle
    if Writer.Config.CHAPTER_NO_REVISIONS:
        _Logger.Log(f"Chapter Revision Disabled In Config, Exiting Now", 5)
        return Chapter

    _Logger.Log(
        f"Entering Feedback/Revision Loop (Stage 5) For Chapter {_ChapterNum}/{_TotalChapters}",
        4,
    )
    WritingHistory = MesssageHistory.copy()
    Rating: int = 0
    Iterations: int = 0
    while True:
        Iterations += 1
        Feedback = Writer.LLMEditor.GetFeedbackOnChapter(Interface, _Logger, Chapter, _Outline)
        Rating = Writer.LLMEditor.GetChapterRating(Interface, _Logger, Chapter)

        if Iterations > Writer.Config.CHAPTER_MAX_REVISIONS:
            break
        if (Iterations > Writer.Config.CHAPTER_MIN_REVISIONS) and (Rating == True):
            break
        Chapter, WritingHistory = ReviseChapter(Interface, _Logger, Chapter, Feedback, WritingHistory)

    _Logger.Log(f"Quality Standard Met, Exiting Feedback/Revision Loop (Stage 5) For Chapter {_ChapterNum}/{_TotalChapters}", 4)

    return Chapter


def ReviseChapter(Interface, _Logger, _Chapter, _Feedback, _History: list = []):

    RevisionPrompt = f"""
Please revise the following chapter:

<CHAPTER_CONTENT>
{_Chapter}
</CHAPTER_CONTENT>

Based on the following feedback:
<FEEDBACK>
{_Feedback}
</FEEDBACK>
Do not reflect on the revisions, just write the improved chapter that addresses the feedback and prompt criteria.  
Remember not to include any author notes.  

"""

    _Logger.Log("Revising Chapter", 5)
    Messages = _History
    Messages.append(Interface.BuildUserQuery(RevisionPrompt))
    Messages = Interface.ChatAndStreamResponse(
        _Logger, Messages, Writer.Config.CHAPTER_REVISION_WRITER_MODEL
    )
    SummaryText: str = Interface.GetLastMessageText(Messages)
    _Logger.Log("Done Revising Chapter", 5)

    return SummaryText, Messages
