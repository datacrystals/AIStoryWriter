import Writer.LLMEditor
import Writer.PrintUtils
import Writer.Config
import Writer.Chapter.ChapterGenSummaryCheck
import Writer.Prompts
import Writer.Scene.ChapterOutlineToScenes
import Writer.Scene.ScenesToJSON
import Writer.Scene.SceneOutlineToScene



def ChapterByScene(Interface, _Logger, _ThisChapter:str, _Outline:str, _BaseContext:str = ""):

    # This function calls all other scene-by-scene generation functions and creates a full chapter based on the new scene pipeline.

    _Logger.Log(f"Starting Scene-By-Scene Chapter Generation Pipeline", 2)

    SceneBySceneOutline = Writer.Scene.ChapterOutlineToScenes.ChapterOutlineToScenes(Interface, _Logger, _ThisChapter, _Outline, _BaseContext=_BaseContext)

    SceneJSONList = Writer.Scene.ScenesToJSON.ScenesToJSON(Interface, _Logger, SceneBySceneOutline)


    # Now we iterate through each scene one at a time and write it, then add it to this rough chapter, which is then returned for further editing
    RoughChapter:str = ""
    for Scene in SceneJSONList:
        RoughChapter += Writer.Scene.SceneOutlineToScene.SceneOutlineToScene(Interface, _Logger, Scene, _Outline, _BaseContext)


    _Logger.Log(f"Starting Scene-By-Scene Chapter Generation Pipeline", 2)

    return RoughChapter
