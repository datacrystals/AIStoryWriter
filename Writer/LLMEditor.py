import Writer.OllamaInterface
import Writer.PrintUtils

import json


def GetFeedbackOnOutline(_Client, _Outline:str):

    StartingPrompt:str = "Please critique the following outline - make sure to provide constructive criticism on how it can be improved and point out any problems with it."
    StartingPrompt += "\n\n\n"
    StartingPrompt += _Outline

    Writer.PrintUtils.PrintBanner("Prompting LLM To Critique Outline", "green")
    Messages = [Writer.OllamaInterface.BuildUserQuery(StartingPrompt)]
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages)
    Writer.PrintUtils.PrintBanner("Finished Getting Feedback", "green")

    return Writer.OllamaInterface.GetLastMessageText(Messages)


def GetOutlineRating(_Client, _Outline:str):

    StartingPrompt:str = _Outline
    StartingPrompt += "\n\n\n"
    StartingPrompt += "Review the above outline honestly, and give a json formatted response, containing the string \"OverallRating\", followed by an integer from 1-100. Please do not include any other text, just the JSON as your response will be parsed by a computer."

    Writer.PrintUtils.PrintBanner("Prompting LLM To Get Review JSON", "green")
    Messages = [Writer.OllamaInterface.BuildUserQuery(StartingPrompt)]
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages)
    Writer.PrintUtils.PrintBanner("Finished Getting Review JSON", "green")


    while True:
        
        RawResponse = Writer.OllamaInterface.GetLastMessageText(Messages)
        
        try:
            Rating = json.loads(RawResponse)["OverallRating"]
            Writer.PrintUtils.PrintBanner(f"Editor Reviewed Outline At {Rating}/100", "green")
            return Rating
        except Exception as E:
            Writer.PrintUtils.PrintBanner("Error Parsing JSON Written By LLM, Asking For Edits", "red")
            EditPrompt:str = f"Please revise your JSON. It encountered the following error during parsing: {E}."
            Messages.append(Writer.OllamaInterface.BuildUserQuery(EditPrompt))
            Writer.PrintUtils.PrintBanner("Asking LLM TO Revise", "red")
            Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages)
            Writer.PrintUtils.PrintBanner("Done Asking LLM TO Revise", "red")
