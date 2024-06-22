import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.Config

def EditNovel(_Client, _Logger, _Chapters:list, _Outline:str, _TotalChapters:int):

    EditedChapters = _Chapters

    for i in range(1, _TotalChapters + 1):

        NovelText:str = ""
        for Chapter in EditedChapters:
            NovelText += Chapter

        Prompt:str = f"""
Outline:
```
{_Outline}
```

Novel:
```
{NovelText}
```

Given the above novel and outline, please edit chapter {i} so that it fits together with the rest of the story.
"""
        _Logger.Log(f"Prompting LLM To Perform Chapter {i} Second Pass In-Place Edit", 5)
        Messages = []
        Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))
        Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.CHAPTER_WRITER_MODEL)
        _Logger.Log(f"Finished Chapter {i} Second Pass In-Place Edit", 5)

        NewChapter = Writer.OllamaInterface.GetLastMessageText(Messages)
        EditedChapters[i] = NewChapter
        ChapterWordCount = Writer.Statistics.GetWordCount(NewChapter)
        _Logger.Log(f"New Chapter Word Count: {ChapterWordCount}", 3)

    return EditedChapters