import Writer.Config
import Writer.OllamaInterface

import json



def GetStoryInfo(_Client, _Messages:list):

    Prompt:str = f"""
Please write a JSON formatted response with no other content with the following keys.
Note that a computer is parsing this JSON so it must be correct.

Base your answers on the story written in previous messages.

"Title": (a short title that's three to eight words)
"Summary": (a paragraph that summarizes the story)
"Tags": (a string of tags separated by commas that describe the story)
"OverallRating": (your overall score for the story from 0-100)

Again, remember to make your response JSON formatted with no extra words. It will be fed directly to a JSON parser.
"""
    
    Writer.PrintUtils.PrintBanner("Prompting LLM To Generate Stats", "green")
    Messages = _Messages
    Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.INFO_MODEL)
    Writer.PrintUtils.PrintBanner("Finished Getting Stats Feedback", "green")

    Dict = json.loads(Writer.OllamaInterface.GetLastMessageText(Messages))


    while True:
        
        RawResponse = Writer.OllamaInterface.GetLastMessageText(Messages)
        RawResponse.replace("`", "")
        RawResponse.replace("json", "")

        try:
            Dict = json.loads(RawResponse)
            return Dict
        except Exception as E:
            Writer.PrintUtils.PrintBanner("Error Parsing JSON Written By LLM, Asking For Edits", "red")
            EditPrompt:str = f"Please revise your JSON. It encountered the following error during parsing: {E}."
            Messages.append(Writer.OllamaInterface.BuildUserQuery(EditPrompt))
            Writer.PrintUtils.PrintBanner("Asking LLM TO Revise", "red")
            Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.INFO_MODEL)
            Writer.PrintUtils.PrintBanner("Done Asking LLM TO Revise", "red")


