import Writer.LLMEditor
import Writer.PrintUtils
import Writer.Config
import Writer.Chapter.ChapterGenSummaryCheck
import Writer.Prompts


def ChapterOutlineToScenes(Interface, _Logger, _ThisChapter:str, _Outline:str, _BaseContext: str = ""):

    # We're now going to convert the chapter outline into a more detailed outline for each scene.
    # The scene by scene outline will be returned, JSONified, and then later converted into fully written scenes
    # These will then be concatenated into chapters and revised


    _Logger.Log(f"Splitting Chapter Into Scenes", 2)
    MesssageHistory: list = []
    MesssageHistory.append(Interface.BuildSystemQuery(Writer.Prompts.DEFAULT_SYSTEM_PROMPT))
    MesssageHistory.append(Interface.BuildUserQuery(Writer.Prompts.CHAPTER_TO_SCENES.format(_ThisChapter=_ThisChapter, _Outline=_Outline)))

    Response = Interface.SafeGenerateText(_Logger, MesssageHistory, Writer.Config.CHAPTER_OUTLINE_WRITER_MODEL, _MinWordCount=200)
    _Logger.Log(f"Finished Splitting Chapter Into Scenes", 5)

    return Interface.GetLastMessageText(Response)
