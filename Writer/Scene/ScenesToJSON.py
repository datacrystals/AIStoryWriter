import Writer.LLMEditor
import Writer.PrintUtils
import Writer.Config
import Writer.Chapter.ChapterGenSummaryCheck
import Writer.Prompts


def ScenesToJSON(Interface, _Logger, _Scenes:str):

    # This function converts the given scene list (from markdown format, to a specified JSON format).

    _Logger.Log(f"Starting ChapterScenes->JSON", 2)
    MesssageHistory: list = []
    MesssageHistory.append(Interface.BuildSystemQuery(Writer.Prompts.DEFAULT_SYSTEM_PROMPT))
    MesssageHistory.append(Interface.BuildUserQuery(Writer.Prompts.SCENES_TO_JSON.format(_Scenes=_Scenes)))

    _, SceneList = Interface.SafeGenerateJSON(_Logger, MesssageHistory, Writer.Config.CHECKER_MODEL)
    _Logger.Log(f"Finished ChapterScenes->JSON ({len(SceneList)} Scenes Found)", 5)

    return SceneList
