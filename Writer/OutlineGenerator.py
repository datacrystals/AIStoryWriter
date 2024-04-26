import Writer.LLMEditor
import Writer.OllamaInterface
import Writer.PrintUtils


def ReviseOutline(_Client, _Outline, _Feedback):

    RevisionPrompt = "Please revise the following outline:\n\n"
    RevisionPrompt += _Outline
    RevisionPrompt += "\n\nBased on the following feedback:\n\n"
    RevisionPrompt += _Feedback

    Writer.PrintUtils.PrintBanner("Revising Outline", "green")
    Messages = [Writer.OllamaInterface.BuildUserQuery(RevisionPrompt)]
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages)
    SummaryText:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner("Done Revising Outline", "green")

    return SummaryText



def GenerateOutline(_Client, _OutlinePrompt, _QualityThreshold:int = 85):

    Prompt = "Please write a markdown formatted outline based on the following prompt:\n\n"
    Prompt += _OutlinePrompt

    # Generate Initial Outline
    Writer.PrintUtils.PrintBanner("Generating Initial Outline", "green")
    Messages = [Writer.OllamaInterface.BuildUserQuery(Prompt)]
    Messages = Writer.OllamaInterface.ChatAndStreamResponse(_Client, Messages)
    Outline:str = Writer.OllamaInterface.GetLastMessageText(Messages)
    Writer.PrintUtils.PrintBanner("Done Generating Initial Outline", "green")

    
    Writer.PrintUtils.PrintBanner("Entering Feedback/Revision Loop", "yellow")
    Rating:int = 0
    while Rating < _QualityThreshold:
        Feedback = Writer.LLMEditor.GetFeedbackOnOutline(_Client, Outline)
        Rating = Writer.LLMEditor.GetOutlineRating(_Client, Outline)

        Outline = ReviseOutline(Outline, Feedback)

    Writer.PrintUtils.PrintBanner("Quality Standard Met, Exiting Feedback/Revision Loop", "yellow")

    return Outline

    