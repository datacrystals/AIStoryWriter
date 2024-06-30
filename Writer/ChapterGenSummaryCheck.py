import json

import Writer.LLMEditor
import Writer.PrintUtils
import Writer.Config
import Writer.Prompts


def LLMSummaryCheck(Interface, _Logger, _RefSummary: str, _Work: str):
    """
    Generates a summary of the work provided, and compares that to the reference summary, asking if they answered the prompt correctly.
    """

    # LLM Length Check - Firstly, check if the length of the response was at least 100 words.
    if len(_Work.split(" ")) < 100:
        _Logger.Log(
            "Previous response didn't meet the length requirement, so it probably tried to cheat around writing.",
            7,
        )
        return False, ""

    # Build Summariziation Langchain
    SummaryLangchain: list = []
    SummaryLangchain.append(
        Interface.BuildSystemQuery(Writer.Prompts.SUMMARY_CHECK_INTRO)
    )
    SummaryLangchain.append(
        Interface.BuildUserQuery(
            Writer.Prompts.SUMMARY_CHECK_PROMPT.format(_Work=_Work)
        )
    )
    SummaryLangchain = Interface.ChatAndStreamResponse(
        _Logger, SummaryLangchain, Writer.Config.CHAPTER_STAGE1_WRITER_MODEL
    )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
    WorkSummary: str = Interface.GetLastMessageText(SummaryLangchain)

    # Now Summarize The Outline
    SummaryLangchain: list = []
    SummaryLangchain.append(
        Interface.BuildSystemQuery(Writer.Prompts.SUMMARY_OUTLINE_INTRO)
    )
    SummaryLangchain.append(
        Interface.BuildUserQuery(
            Writer.Prompts.SUMMARY_OUTLINE_PROMPT.format(_RefSummary=_RefSummary)
        )
    )
    SummaryLangchain = Interface.ChatAndStreamResponse(
        _Logger, SummaryLangchain, Writer.Config.CHAPTER_STAGE1_WRITER_MODEL
    )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!
    OutlineSummary: str = Interface.GetLastMessageText(SummaryLangchain)

    # Now, generate a comparison JSON value.
    ComparisonLangchain: list = []
    ComparisonLangchain.append(
        Interface.BuildSystemQuery(Writer.Prompts.SUMMARY_COMPARE_INTRO)
    )
    ComparisonLangchain.append(
        Interface.BuildUserQuery(
            Writer.Prompts.SUMMARY_COMPARE_PROMPT.format(
                WorkSummary=WorkSummary, OutlineSummary=OutlineSummary
            )
        )
    )
    ComparisonLangchain = Interface.ChatAndStreamResponse(
        _Logger, ComparisonLangchain, Writer.Config.REVISION_MODEL, _Format="json"
    )  # CHANGE THIS MODEL EVENTUALLY - BUT IT WORKS FOR NOW!!!

    Iters: int = 0
    while True:

        RawResponse = Interface.GetLastMessageText(ComparisonLangchain)
        RawResponse = RawResponse.replace("`", "")
        RawResponse = RawResponse.replace("json", "")

        try:
            Iters += 1
            Dict = json.loads(RawResponse)
            return (
                Dict["DidFollowOutline"],
                "### Extra Suggestions:\n" + Dict["Suggestions"],
            )
        except Exception as E:
            if Iters > 4:
                _Logger.Log("Critical Error Parsing JSON", 7)
                return False, ""

            _Logger.Log("Error Parsing JSON Written By LLM, Asking For Edits", 7)
            EditPrompt: str = (
                f"Please revise your JSON. It encountered the following error during parsing: {E}. Remember that your entire response is plugged directly into a JSON parser, so don't write **anything** except pure json."
            )
            ComparisonLangchain.append(Interface.BuildUserQuery(EditPrompt))
            _Logger.Log("Asking LLM TO Revise", 7)
            ComparisonLangchain = Interface.ChatAndStreamResponse(
                _Logger,
                ComparisonLangchain,
                Writer.Config.CHECKER_MODEL,
                _Format="json",
            )
            _Logger.Log("Done Asking LLM TO Revise JSON", 6)
