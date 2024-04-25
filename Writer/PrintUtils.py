import termcolor


def PrintBanner(_Text, _Color="green", _Banner=True):

    FinalText = " - " + _Text

    BannerBlock = ""
    for i in range(len(FinalText)):
        BannerBlock += "="

    if _Banner:
        print(termcolor.colored(BannerBlock, _Color))
    
    print(termcolor.colored(FinalText, _Color))

    if _Banner:
        print(termcolor.colored(BannerBlock, _Color))

