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

Also, please check if the outline is written chapter-by-chapter, not in sections spanning multiple chapters or subsections.
It should be very clear which chapter is which, and the content in each chapter.

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
This outline meets all of the following criteria (true or false):
    - Pacing: Is the story rushing over certain plot points and excessively focusing on others?
    - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?
    - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
    - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?

Give a JSON formatted response, containing the string \"IsComplete\", followed by an boolean True/False.
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
            Rating = json.loads(RawResponse)["IsComplete"]
            Writer.PrintUtils.PrintBanner(f"Editor Determined IsComplete: {Rating}", "green")
            return Rating, Messages
        except Exception as E:
            Writer.PrintUtils.PrintBanner("Error Parsing JSON Written By LLM, Asking For Edits", "red")
            EditPrompt:str = f"Please revise your JSON. It encountered the following error during parsing: {E}."
            Messages.append(Writer.OllamaInterface.BuildUserQuery(EditPrompt))
            Writer.PrintUtils.PrintBanner("Asking LLM TO Revise", "red")
            Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.EVAL_MODEL)
            Writer.PrintUtils.PrintBanner("Done Asking LLM TO Revise", "red")





def GetFeedbackOnChapter(_Client, _Chapter:str, _Outline:str, _History:list = []):

    # Disabled seeing the outline too.
    StartingPrompt:str = f"""
Chapter:
```
{_Chapter}
```

Please give feedback on the above chapter based on the following criteria:
    - Pacing: Is the story rushing over certain plot points and excessively focusing on others?
    - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?
    - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
    - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?
    
    - Characters: Who are the characters in this chapter? What do they mean to each other? What is the situation between them? Is it a conflict? Is there tension? Is there a reason that the characters have been brought together?
    - Development:  What are the goals of each character, and do they meet those goals? Do the characters change and exhibit growth? Do the goals of each character change over the story?
    
    - Dialogue: Does the dialogue make sense? Is it appropriate given the situation? Does the pacing make sense for the scene E.g: (Is it fast-paced because they're running, or slow-paced because they're having a romantic dinner)? 
    - Disruptions: If the flow of dialogue is disrupted, what is the reason for that disruption? Is it a sense of urgency? What is causing the disruption? How does it affect the dialogue moving forwards? 

"""

    Writer.PrintUtils.PrintBanner("Prompting LLM To Critique Chapter", "green")
    Messages = _History
    Messages.append(Writer.OllamaInterface.BuildUserQuery(StartingPrompt))
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.REVISION_MODEL)
    Writer.PrintUtils.PrintBanner("Finished Getting Chapter Feedback", "green")

    return Writer.OllamaInterface.GetLastMessageText(Messages), Messages


# Switch this to iscomplete true/false (similar to outline)
def GetChapterRating(_Client, _Chapter:str, _History:list = []):

    StartingPrompt:str = f"""
{_Chapter}

---
This chapter meets all of the following criteria (true or false):
    - Pacing: Is the story rushing over certain plot points and excessively focusing on others?
    - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?
    - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
    - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?

Give a JSON formatted response, containing the string \"IsComplete\", followed by an boolean True/False.
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
            Rating = json.loads(RawResponse)["IsComplete"]
            Writer.PrintUtils.PrintBanner(f"Editor Determined IsComplete: {Rating}", "green")
            return Rating, Messages
        except Exception as E:
            Writer.PrintUtils.PrintBanner("Error Parsing JSON Written By LLM, Asking For Edits", "red")
            EditPrompt:str = f"Please revise your JSON. It encountered the following error during parsing: {E}."
            Messages.append(Writer.OllamaInterface.BuildUserQuery(EditPrompt))
            Writer.PrintUtils.PrintBanner("Asking LLM TO Revise", "red")
            Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages, Writer.Config.EVAL_MODEL)
            Writer.PrintUtils.PrintBanner("Done Asking LLM TO Revise", "red")
