import json

import Writer.LLMEditor
import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.Config





def LLMSummaryCheck(_Client, _Logger, _RefSummary:str , _Work:str):
    '''
    Generates a summary of the work provided, and compares that to the reference summary, asking if they answered the prompt correctly.
    '''

    # LLM Length Check - Firstly, check if the length of the response was at least 100 words.
    if (len(_Work.split(" ")) < 100):
        _Logger.Log("Previous response didn't meet the length requirement, so it probably tried to cheat around writing.", 7)
        return False, ""

    # Build Summariziation Langchain
    SummaryLangchain:list = []
    SummaryLangchain.append(Writer.OllamaInterface.BuildSystemQuery(f"You are a helpful AI Assistant. Answer the user's prompts to the best of your abilities."))
    SummaryLangchain.append(Writer.OllamaInterface.BuildUserQuery(f"""
Please summarize the following chapter:
                                                                  
<CHAPTER>
{_Work}
</CHAPTER>

Do not include anything in your response except the summary.

"""))
    SummaryLangchain = Writer.OllamaInterface.ChatAndStreamResponse(_Client, _Logger, SummaryLangchain, Writer.Config.CHAPTER_STAGE1_WRITER_MODEL) # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
    WorkSummary:str = Writer.OllamaInterface.GetLastMessageText(SummaryLangchain)


    # Now, generate a comparison JSON value.
    ComparisonLangchain:list = []
    ComparisonLangchain.append(Writer.OllamaInterface.BuildSystemQuery(f"You are a helpful AI Assistant. Answer the user's prompts to the best of your abilities."))
    ComparisonLangchain.append(Writer.OllamaInterface.BuildUserQuery(f"""
Please compare the provided summary of a chapter and the associated outline, and indicate if the provided content matches the outline.
                                                                     
Please write a JSON formatted response with no other content with the following keys.
Note that a computer is parsing this JSON so it must be correct.

<CHAPTER_SUMMARY>
{WorkSummary}
</CHAPTER_SUMMARY>
                                                                     
<OUTLINE>
{_RefSummary}
</OUTLINE>

Please indicate if they did or did not by responding with the following JSON fields:

"DidFollowOutline": true/false
"Suggestions": str


Did it write the correct chapter? Sometimes it'll get confused and write the wrong chapter (usually one more than the current one).

Suggestions should include a string containing markdown formatted feedback that will be used to prompt the LLM on the next iteration of generation.
Specify general things that would help the LLM remember what to do in the next generation.
It will not see the current chapter, so feedback specific to this one is not helpful, instead specify areas where it needs to pay attention to either the prompt or outline.

Again, remember to make your response JSON formatted with no extra words. It will be fed directly to a JSON parser.
"""))
    ComparisonLangchain = Writer.OllamaInterface.ChatAndStreamResponse(_Client, _Logger, ComparisonLangchain, Writer.Config.REVISION_MODEL) # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!


    while True:
        
        RawResponse = Writer.OllamaInterface.GetLastMessageText(ComparisonLangchain)
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")

        try:
            Dict = json.loads(RawResponse)
            return Dict["DidFollowOutline"], "### Extra Suggestions:\n" + Dict["Suggestions"]
        except Exception as E:
            _Logger.Log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            EditPrompt:str = f"Please revise your JSON. It encountered the following error during parsing: {E}."
            ComparisonLangchain.append(Writer.OllamaInterface.BuildUserQuery(EditPrompt))
            _Logger.Log("Asking LLM TO Revise", 7)
            ComparisonLangchain = Writer.OllamaInterface.ChatAndStreamResponse(_Client, _Logger, ComparisonLangchain, Writer.Config.CHECKER_MODEL)
            _Logger.Log("Done Asking LLM TO Revise JSON", 6)

