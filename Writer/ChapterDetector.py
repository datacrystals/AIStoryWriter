import Writer.Config
import Writer.OllamaInterface

import re
import json



def LLMCountChapters(_Client, _Summary):

    Prompt = f"""
Outline:
---
{_Summary}
---

Please provide a JSON formatted response containing the total number of chapters in the above outline.

Respond with "TotalChapters": <total chapter count>.
Please do not include any other text, just the JSON as your response will be parsed by a computer.

"""
    


    Writer.PrintUtils.PrintBanner("Prompting LLM To Get ChapterCount JSON", "green")
    Messages = []
    Messages.append(Writer.OllamaInterface.BuildUserQuery(Prompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.EVAL_MODEL)
    Writer.PrintUtils.PrintBanner("Finished Getting ChapterCount JSON", "green")


    while True:
        
        RawResponse = Writer.OllamaInterface.GetLastMessageText(Messages)
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")

        try:
            TotalChapters = json.loads(RawResponse)["TotalChapters"]
            Writer.PrintUtils.PrintBanner(f"Got Total Chapter Count At {TotalChapters}", "green")
            return TotalChapters
        except Exception as E:
            Writer.PrintUtils.PrintBanner("Error Parsing JSON Written By LLM, Asking For Edits", "red")
            EditPrompt:str = f"Please revise your JSON. It encountered the following error during parsing: {E}."
            Messages.append(Writer.OllamaInterface.BuildUserQuery(EditPrompt))
            Writer.PrintUtils.PrintBanner("Asking LLM TO Revise", "red")
            Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.EVAL_MODEL)
            Writer.PrintUtils.PrintBanner("Done Asking LLM TO Revise", "red")





def CountChapters(_Summary):

    Pattern = re.compile('chapter [0-9]*')

    LowerText = _Summary.lower()
    Matches = Pattern.findall(LowerText)

    if (len(Matches) == 0):
        print("Error! Could not find any matches!")
        return 0
    

    NumChapters:int = 0

    # Find all the ones with 
    for Match in Matches:

        # Get the number portion, find the highest chapter number, that's our chapter total count
        try:
            ChapterNumber = int(Match.replace("chapter ", ""))

            if (ChapterNumber > NumChapters):
                NumChapters = ChapterNumber
        except:
            pass

    return NumChapters