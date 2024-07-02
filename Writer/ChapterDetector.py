import Writer.Config
import Writer.Prompts

import re
import json


def LLMCountChapters(Interface, _Logger, _Summary):

    Prompt = Writer.Prompts.CHAPTER_COUNT_PROMPT.format(_Summary=_Summary)

    _Logger.Log("Prompting LLM To Get ChapterCount JSON", 5)
    Messages = []
    Messages.append(Interface.BuildUserQuery(Prompt))
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.EVAL_MODEL, _Format="json"
    )
    _Logger.Log("Finished Getting ChapterCount JSON", 5)

    Iters: int = 0

    while True:

        RawResponse = Interface.GetLastMessageText(Messages)
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
            EditPrompt: str = (
                f"Please revise your JSON. It encountered the following error during parsing: {E}. Remember that your entire response is plugged directly into a JSON parser, so don't write **anything** except pure json."
            )
            Messages.append(Interface.BuildUserQuery(EditPrompt))
            _Logger.Log("Asking LLM TO Revise", 7)
            Messages = Interface.SafeGenerateText(
                _Logger, Messages, Writer.Config.EVAL_MODEL, _Format="json"
            )
            _Logger.Log("Done Asking LLM TO Revise JSON", 6)
