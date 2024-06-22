import Writer.OllamaInterface
import Writer.PrintUtils



def ScrubNovel(_Client, _Logger, _Chapters:list, _TotalChapters:int):

    EditedChapters = _Chapters

    for i in range(_TotalChapters):


        Prompt:str = f"""

Chapter:
```
{_Chapters[i]}
```

Given the above chapter, please clean it up so that it is ready to be published.
That is, please remove any leftover outlines or editorial comments only leaving behind the finished story.

Do not comment on your task, as your output will be the final print version.
"""
        _Logger.Log(f"Prompting LLM To Perform Chapter {i+1} Scrubbing Edit", 5)
        Messages = []
        Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))
        Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.SCRUB_MODEL)
        _Logger.Log(f"Finished Chapter {i+1} Scrubbing Edit", 5)

        NewChapter = Writer.OllamaInterface.GetLastMessageText(Messages)
        EditedChapters[i] = NewChapter
        ChapterWordCount = Writer.Statistics.GetWordCount(NewChapter)
        _Logger.Log(f"Scrubbed Chapter Word Count: {ChapterWordCount}", 3)

    return EditedChapters