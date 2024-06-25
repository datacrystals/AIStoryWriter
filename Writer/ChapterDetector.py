import Writer.Config
import Writer.OllamaInterface

import re
import json



def LLMCountChapters(_Client, _Logger, _Summary):

    Prompt = f"""
Outline:
---
{_Summary}
---

Please provide a JSON formatted response containing the total number of chapters in the above outline.

Respond with {{"TotalChapters": <total chapter count>}}
Please do not include any other text, just the JSON as your response will be parsed by a computer.

"""
    

    _Logger.Log("Prompting LLM To Get ChapterCount JSON", 5)
    Messages = []
    Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, _Logger, Messages, Writer.Config.EVAL_MODEL)
    _Logger.Log("Finished Getting ChapterCount JSON", 5)

    Iters:int = 0

    while True:
        
        RawResponse = Writer.OllamaInterface.GetLastMessageText(Messages)
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")

        try:
            Iters += 1
            TotalChapters = json.loads(RawResponse)["TotalChapters"]
            _Logger.Log("Got Total Chapter Count At {TotalChapters}", 5)
            return TotalChapters
        except Exception as E:
            if Iters > 4:
                _Logger.Log("Critical Error Parsing JSON", 7)
                return -1
            _Logger.Log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            EditPrompt:str = f"Please revise your JSON. It encountered the following error during parsing: {E}. Remember that your entire response is plugged directly into a JSON parser, so don't write **anything** except pure json."
            Messages.append(Writer.OllamaInterface.BuildUserQuery(EditPrompt))
            _Logger.Log("Asking LLM TO Revise", 7)
            Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, _Logger, Messages, Writer.Config.EVAL_MODEL)
            _Logger.Log("Done Asking LLM TO Revise JSON", 6)
