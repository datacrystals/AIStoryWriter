import Writer.OllamaInterface
import Writer.PrintUtils



def ScrubNovel(_Client, _Chapters:list, _TotalChapters:int):

    EditedChapters = _Chapters

    for i in range(1, _TotalChapters + 1):


        Prompt:str = f"""

Chapter:
```
{_Chapters[i]}
```

Given the above chapter, please clean it up so that it is ready to be published.
That is, please remove any leftover outlines or editorial comments only leaving behind the finished story.
"""
        Writer.PrintUtils.PrintBanner(f"Prompting LLM To Perform Chapter {i} Scrubbing Edit", "green")
        Messages = []
        Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))
        Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.SCRUB_MODEL)
        Writer.PrintUtils.PrintBanner(f"Finished Chapter {i} Scrubbing Edit", "green")

        NewChapter = Writer.OllamaInterface.GetLastMessageText(Messages)
        EditedChapters[i] = NewChapter
        ChapterWordCount = Writer.Statistics.GetWordCount(NewChapter)
        Writer.PrintUtils.PrintBanner(f"Scrubbed Chapter Word Count: {ChapterWordCount}", "blue")

    return EditedChapters