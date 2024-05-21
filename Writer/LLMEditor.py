import Writer.OllamaInterface
import Writer.PrintUtils

import json


def GetFeedbackOnOutline(_Client, _Outline:str, _History:list = []):

    StartingPrompt:str = f"""
Please critique the following outline - make sure to provide constructive criticism on how it can be improved and point out any problems with it.

---
{_Outline}
---

As you revise, consider the following criteria:
    - Pacing: Is the story rushing over certain plot points and excessively focusing on others?
    - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?
    - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
    - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?

    """

    Writer.PrintUtils.PrintBanner("Prompting LLM To Critique Outline", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(StartingPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.REVISION_MODEL)
    Writer.PrintUtils.PrintBanner("Finished Getting Outline Feedback", "green")

    return Writer.OllamaInterface.GetLastMessageText(Messages), Messages


def GetOutlineRating(_Client, _Outline:str, _History:list = []):

    StartingPrompt:str = f"""
{_Outline}

---

Review the above outline honestly, and give a json formatted response, containing the string \"OverallRating\", followed by an integer from 1-100.
Please do not include any other text, just the JSON as your response will be parsed by a computer.
"""

    Writer.PrintUtils.PrintBanner("Prompting LLM To Get Review JSON", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(StartingPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.EVAL_MODEL)
    Writer.PrintUtils.PrintBanner("Finished Getting Review JSON", "green")


    while True:
        
        RawResponse = Writer.OllamaInterface.GetLastMessageText(Messages)
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")

        try:
            Rating = json.loads(RawResponse)["OverallRating"]
            Writer.PrintUtils.PrintBanner(f"Editor Reviewed Outline At {Rating}/100", "green")
            return Rating, Messages
        except Exception as E:
            Writer.PrintUtils.PrintBanner("Error Parsing JSON Written By LLM, Asking For Edits", "red")
            EditPrompt:str = f"Please revise your JSON. It encountered the following error during parsing: {E}."
            Messages.append(Writer.OllamaInterface.BuildUserQuery(EditPrompt))
            Writer.PrintUtils.PrintBanner("Asking LLM TO Revise", "red")
            Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.EVAL_MODEL)
            Writer.PrintUtils.PrintBanner("Done Asking LLM TO Revise", "red")





def GetFeedbackOnChapter(_Client, _Chapter:str, _Outline:str, _History:list = []):

    StartingPrompt:str = f"""
Chapter:
```
{_Chapter}
```

Outline:
```
{_Outline}
```

You are a professional editor.
Please critique the previously mentioned chapter, and suggest improvements for clarity and substance.
Make sure the chapter follows the outline so that the story stays on track!

"""

    Writer.PrintUtils.PrintBanner("Prompting LLM To Critique Chapter", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(StartingPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.REVISION_MODEL)
    Writer.PrintUtils.PrintBanner("Finished Getting Chapter Feedback", "green")

    return Writer.OllamaInterface.GetLastMessageText(Messages), Messages


def GetChapterRating(_Client, _Chapter:str, _History:list = []):

    StartingPrompt:str = f"""
{_Chapter}

---
Review the above chapter honestly, and give a json formatted response, containing the string \"OverallRating\", followed by an integer from 1-100.
Please do not include any other text, just the JSON as your response will be parsed by a computer.
"""

    Writer.PrintUtils.PrintBanner("Prompting LLM To Get Review JSON", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(StartingPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.EVAL_MODEL)
    Writer.PrintUtils.PrintBanner("Finished Getting Review JSON", "green")


    while True:
        
        RawResponse = Writer.OllamaInterface.GetLastMessageText(Messages)
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")
        
        try:
            Rating = json.loads(RawResponse)["OverallRating"]
            Writer.PrintUtils.PrintBanner(f"Editor Reviewed Chapter At {Rating}/100", "green")
            return Rating, Messages
        except Exception as E:
            Writer.PrintUtils.PrintBanner("Error Parsing JSON Written By LLM, Asking For Edits", "red")
            EditPrompt:str = f"Please revise your JSON. It encountered the following error during parsing: {E}."
            Messages.append(Writer.OllamaInterface.BuildUserQuery(EditPrompt))
            Writer.PrintUtils.PrintBanner("Asking LLM TO Revise", "red")
            Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.EVAL_MODEL)
            Writer.PrintUtils.PrintBanner("Done Asking LLM TO Revise", "red")
