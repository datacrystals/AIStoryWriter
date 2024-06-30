import Writer.PrintUtils
import Writer.Prompts


def ScrubNovel(Interface, _Logger, _Chapters: list, _TotalChapters: int):

    EditedChapters = _Chapters

    for i in range(_TotalChapters):

        Prompt: str = Writer.Prompts.CHAPTER_SCRUB_PROMPT.format(
            _Chapter=EditedChapters[i]
        )
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
