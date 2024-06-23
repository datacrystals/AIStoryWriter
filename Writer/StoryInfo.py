import Writer.Config
import Writer.OllamaInterface

import json



def GetStoryInfo(_Client, _Logger, _Messages:list):

    Prompt:str = f"""
Please write a JSON formatted response with no other content with the following keys.
Note that a computer is parsing this JSON so it must be correct.

Base your answers on the story written in previous messages.

"Title": (a short title that's three to eight words)
"Summary": (a paragraph or two that summarizes the story from start to finish)
"Tags": (a string of tags separated by commas that describe the story)
"OverallRating": (your overall score for the story from 0-100)

Again, remember to make your response JSON formatted with no extra words. It will be fed directly to a JSON parser.
"""
    
    _Logger.Log("Prompting LLM To Generate Stats", 5)
    Messages = _Messages
    Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, _Logger, Messages, Writer.Config.INFO_MODEL)
    _Logger.Log("Finished Getting Stats Feedback", 5)

    while True:
        
        RawResponse = Writer.OllamaInterface.GetLastMessageText(Messages)
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")

        try:
            Dict = json.loads(RawResponse)
            return Dict
        except Exception as E:
            _Logger.Log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            EditPrompt:str = f"Please revise your JSON. It encountered the following error during parsing: {E}."
            Messages.append(Writer.OllamaInterface.BuildUserQuery(EditPrompt))
            _Logger.Log("Asking LLM TO Revise", 7)
            Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, _Logger, Messages, Writer.Config.INFO_MODEL)
            _Logger.Log("Done Asking LLM TO Revise JSON", 6)


