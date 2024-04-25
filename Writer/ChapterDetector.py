import re

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