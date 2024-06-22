import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.Config


def TranslateNovel(_Client, _Logger, _Chapters:list, _TotalChapters:int, _Language:str = "French"):

    EditedChapters = _Chapters

    for i in range(_TotalChapters):


        Prompt:str = f"""

Chapter:
```
{_Chapters[i]}
```

Given the above chapter, please translate it to {_Language}.
"""
        _Logger.Log(f"Prompting LLM To Perform Chapter {i+1} Translation", 5)
        Messages = []
        Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))
        Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, _Logger, Messages, Writer.Config.TRANSLATOR_MODEL)
        _Logger.Log(f"Finished Chapter {i+1} Translation", 5)

        NewChapter = Writer.OllamaInterface.GetLastMessageText(Messages)
        EditedChapters[i] = NewChapter
        ChapterWordCount = Writer.Statistics.GetWordCount(NewChapter)
        _Logger.Log(f"Translation Chapter Word Count: {ChapterWordCount}", 3)

    return EditedChapters