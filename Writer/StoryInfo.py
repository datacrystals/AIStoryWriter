import Writer.Config
import json


def GetStoryInfo(Interface, _Logger, _Messages: list):

    Prompt: str = f"""
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
    Messages.append(Interface.BuildUserQuery(Prompt))
    Messages = Interface.ChatAndStreamResponse(
        _Logger, Messages, Writer.Config.INFO_MODEL, _Format="json"
    )
    _Logger.Log("Finished Getting Stats Feedback", 5)

    Iters: int = 0
    while True:

        RawResponse = Interface.GetLastMessageText(Messages)
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")

        try:
            Iters += 1
            Dict = json.loads(RawResponse)
            return Dict
        except Exception as E:
            if Iters > 4:
                _Logger.Log("Critical Error Parsing JSON", 7)
                return {}
            _Logger.Log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            EditPrompt: str = (
                f"Please revise your JSON. It encountered the following error during parsing: {E}. Remember that your entire response is plugged directly into a JSON parser, so don't write **anything** except pure json."
            )
            Messages.append(Interface.BuildUserQuery(EditPrompt))
            _Logger.Log("Asking LLM TO Revise", 7)
            Messages = Interface.ChatAndStreamResponse(
                _Logger, Messages, Writer.Config.INFO_MODEL, _Format="json"
            )
            _Logger.Log("Done Asking LLM TO Revise JSON", 6)
