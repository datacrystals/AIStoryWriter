import Writer.LLMEditor
import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.Config


def GenerateChapter(_Client, _ChapterNum:int, _TotalChapters:int, _Outline:str, _Chapters:list = [], _QualityThreshold:int = 85):


    # Some important notes
    # We're going to remind the author model of the previous chapters here, so it knows what has been written before.

    #### Stage 0: Create base language chain
    MesssageHistory:list = []
    MesssageHistory.append(Writer.OllamaInterface.BuildSystemQuery(f"You are a great fiction writer, and you're working on a great new story. You're working on a new novel, and you want to produce a quality output. Here is your outline: ```{_Outline}```"))
    
    
    
    if (len(_Chapters) > 0):
        MesssageHistory.append(Writer.OllamaInterface.BuildUserQuery("Here is the novel so far."))

        ChapterSuperlist:str = ""
        for Chapter in _Chapters:
            ChapterSuperlist += f"{Chapter}\n"
        MesssageHistory.append(Writer.OllamaInterface.BuildUserQuery(ChapterSuperlist))
        MesssageHistory.append(Writer.OllamaInterface.BuildSystemQuery("Make sure to pay attention to the content that has happened in these previous chapters. It's okay to deviate from the outline a little in order to ensure you continue the same story from previous chapters."))


    #### STAGE 1: Create Initial Plot
    Prompt = f"""
Please write the plot for chapter {_ChapterNum} of {_TotalChapters} based on the following outline and any previous chapters.
Pay attention to the previous chapters, and make sure you both continue seamlessly from them, It's okay to deviate from the outline a bit if needed, just make sure to somewhat follow it (take creative liberties).

As you write your work, please use the following suggestions to help you write:
    - Pacing: 
      - Are you skipping days at a time? Summarizing events? Don't do that, add scenes to detail them.
      - Is the story rushing over certain plot points and excessively focusing on others?
    - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
    - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?

"""

    # Generate Initial Chapter
    Writer.PrintUtils.PrintBanner(f"Generating Initial Chapter (Stage 1: Plot) {_ChapterNum}/{_TotalChapters}", "green")
    Messages = MesssageHistory.copy()
    Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))

    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.CHAPTER_STAGE1_WRITER_MODEL)
    Stage1Chapter:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner(f"Done Generating Initial Chapter (Stage 1: Plot)  {_ChapterNum}/{_TotalChapters}", "green")


    #### STAGE 2: Add Character Development
    Prompt = f"""
Please write character development for the following chapter {_ChapterNum} of {_TotalChapters} based on the following criteria and any previous chapters.
Pay attention to the previous chapters, and make sure you both continue seamlessly from them, It's okay to deviate from the outline a bit if needed, just make sure to somewhat follow it (take creative liberties).

Don't take away content, instead expand upon it to make a longer and more detailed output.

For your reference, here is the outline:
```
{_Outline}
```

And here is the chapter's plot:
```
{Stage1Chapter}
```

As a reminder to keep the following criteria in mind as you expand upon the above work:
    - Characters: Who are the characters in this chapter? What do they mean to each other? What is the situation between them? Is it a conflict? Is there tension? Is there a reason that the characters have been brought together?
    - Development: What are the goals of each character, and do they meet those goals? Do the characters change and exhibit growth? Do the goals of each character change over the story?
    - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?

Don't answer these questions directly, instead make your writing implicitly answer them. (Show, don't tell)

Make sure that your chapter flows into the next and from the previous (if applicable).

Remember, have fun, be creative, and improve the character development of chapter {_ChapterNum}!

"""

    # Generate Initial Chapter
    Writer.PrintUtils.PrintBanner(f"Generating Initial Chapter (Stage 2: Character Development) {_ChapterNum}/{_TotalChapters}", "green")
    Messages = MesssageHistory.copy()
    Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))

    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.CHAPTER_STAGE2_WRITER_MODEL)
    Stage2Chapter:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner(f"Done Generating Initial Chapter (Stage 2: Character Development)  {_ChapterNum}/{_TotalChapters}", "green")


    #### STAGE 3: Add Dialogue
    Prompt = f"""
Please add dialogue the following chapter {_ChapterNum} of {_TotalChapters} based on the following criteria and any previous chapters.
Pay attention to the previous chapters, and make sure you both continue seamlessly from them, It's okay to deviate from the outline a bit if needed, just make sure to somewhat follow it (take creative liberties).

Don't take away content, instead expand upon it to make a longer and more detailed output.

```
{Stage2Chapter}
```

As a reminder to keep the following criteria in mind:
    - Dialogue: Does the dialogue make sense? Is it appropriate given the situation? Does the pacing make sense for the scene E.g: (Is it fast-paced because they're running, or slow-paced because they're having a romantic dinner)? 
    - Disruptions: If the flow of dialogue is disrupted, what is the reason for that disruption? Is it a sense of urgency? What is causing the disruption? How does it affect the dialogue moving forwards? 
     - Pacing: 
       - Are you skipping days at a time? Summarizing events? Don't do that, add scenes to detail them.
       - Is the story rushing over certain plot points and excessively focusing on others?
    
Don't answer these questions directly, instead make your writing implicitly answer them. (Show, don't tell)

Make sure that your chapter flows into the next and from the previous (if applicable).

Remember, have fun, be creative, and add dialogue to chapter {_ChapterNum}!

"""

    # Generate Initial Chapter
    Writer.PrintUtils.PrintBanner(f"Generating Initial Chapter (Stage 3: Dialogue) {_ChapterNum}/{_TotalChapters}", "green")
    Messages = MesssageHistory.copy()
    Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))

    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.CHAPTER_STAGE3_WRITER_MODEL)
    Stage3Chapter:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner(f"Done Generating Initial Chapter (Stage 3: Dialogue)  {_ChapterNum}/{_TotalChapters}", "green")


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
#     Writer.PrintUtils.PrintBanner(f"Generating Initial Chapter (Stage 4: Final Pass) {_ChapterNum}/{_TotalChapters}", "green")
#     Messages = MesssageHistory.copy()
#     Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))

#     Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.CHAPTER_STAGE4_WRITER_MODEL)
#     Chapter:str = Writer.OllamaInterface.GetLastMessageText(Messages)
#     Writer.PrintUtils.PrintBanner(f"Done Generating Initial Chapter (Stage 4: Final Pass)  {_ChapterNum}/{_TotalChapters}", "green")
    Chapter:str = Stage3Chapter


    #### Stage 5: Revision Cycle
    if (Writer.Config.CHAPTER_NO_REVISIONS):
        Writer.PrintUtils.PrintBanner(f"Chapter Revision Disabled In Config, Exiting Now", "green")
        return Chapter


    Writer.PrintUtils.PrintBanner(f"Entering Feedback/Revision Loop (Stage 5) For Chapter {_ChapterNum}/{_TotalChapters}", "yellow")
    FeedbackHistory = []
    WritingHistory = MesssageHistory.copy()
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

    Writer.PrintUtils.PrintBanner(f"Quality Standard Met, Exiting Feedback/Revision Loop (Stage 5) For Chapter {_ChapterNum}/{_TotalChapters}", "yellow")

    return Chapter


def ReviseChapter(_Client, _Chapter, _Feedback, _History:list = []):

    RevisionPrompt = f"""
Please revise the following chapter:
---
{_Chapter}
---
Based on the following feedback:
---
{_Feedback}
---
Do not reflect on the revisions, just write the improved chapter that addresses the feedback and prompt criteria.  
Remember not to include any author notes.  

"""

    Writer.PrintUtils.PrintBanner("Revising Chapter", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(RevisionPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.CHAPTER_REVISION_WRITER_MODEL)
    SummaryText:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner("Done Revising Chapter", "green")

    return SummaryText, Messages


