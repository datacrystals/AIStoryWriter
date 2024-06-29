import Writer.PrintUtils


def ScrubNovel(Interface, _Logger, _Chapters: list, _TotalChapters: int):

    EditedChapters = _Chapters

    for i in range(_TotalChapters):

        Prompt: str = f"""

<CHAPTER>
{_Chapters[i]}
</CHAPTER>

Given the above chapter, please clean it up so that it is ready to be published.
That is, please remove any leftover outlines or editorial comments only leaving behind the finished story.

Do not comment on your task, as your output will be the final print version.
"""
        _Logger.Log(f"Prompting LLM To Perform Chapter {i+1} Scrubbing Edit", 5)
        Messages = []
        Messages.append(Interface.BuildUserQuery(Prompt))
        Messages = Interface.ChatAndStreamResponse(
            _Logger, Messages, Writer.Config.SCRUB_MODEL
        )
        _Logger.Log(f"Finished Chapter {i+1} Scrubbing Edit", 5)

        NewChapter = Interface.GetLastMessageText(Messages)
        EditedChapters[i] = NewChapter
        ChapterWordCount = Writer.Statistics.GetWordCount(NewChapter)
        _Logger.Log(f"Scrubbed Chapter Word Count: {ChapterWordCount}", 3)

    return EditedChapters
