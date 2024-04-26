import Writer.Config
import Writer.OllamaInterface
import Writer.PrintUtils
import Writer.ChapterDetector
import Writer.Statistics
import Writer.OutlineGenerator
import Writer.StoryInfo


# Initialize Client
Writer.PrintUtils.PrintBanner("Created OLLAMA Client", "red")
Client = Writer.OllamaInterface.InitClient("http://10.1.65.4:11434")

StartingPrompt:str = '''
Please outline a 3k word novel about the following prompt. Make 5 chapters.

Alhaitham and Kaveh are both playable characters. They are frequently mentioned throughout character voicelines and Sumeru bulletin boards. The two first met in the House of Daena, and Kaveh had taken interest in his outstanding junior. The two were best friends before walking separate paths after a major quarrel during a large research project. Both Kaveh and Alhaitham graduated from Sumeru Akademiya, Kaveh graduating from the Kshahrewar Darshan while Alhaitham from the Haravatat Darshan. Alhaitham is still a member of this Darshan, and is responsible for documenting their findings and drafting ordinances. Kaveh is a renowned architect and independent contractor who occasionally serves as a visiting professor at the Akademiya and receives subsidies as a result. Despite being a Kshahrewar alumnus, Kaveh is still identified as the Darshan's representative and touts his association with them, which leads to him introducing himself and being introduced as someone that is from the Akademiya. As well, when referring to the Kshahrewar, he at times will use "we." In official media, he is occasionally seen at the Akademiya with what appear to be his students. When Kaveh is a visiting professor at the Akademiya, Alhaitham and Kaveh can be considered coworkers.
After Kaveh sold his family house and went bankrupt because of his dedication to completing his magnum opus, Alhaitham offered him residence. According to the Sumeru bulletin boards, Alhaitham sometimes handles Kaveh's additional fees, such as alcohol fees.
Alhaitham is only interested in studying whatever interests him, having forgone ownership of a supposed Divine Knowledge Capsule to simply study it. He also operates purely by rationality, which many people tend to find unacceptable, especially Kaveh, who is extremely fed up with him. In contrast, Kaveh operates by what he feels is right. He is a stark defender of the arts and believes that helping others is a natural course of action. This contrast has served as an important defining trait to both their characterization, backstories, and relationship, in which they are notably the exact opposite, or mirrors, of one another. Several playable characters and NPCs mention their arguments, and their intense disagreements are such that they even bleed into messages on bulletin boards across Sumeru City and Port Ormos. Messages between Alhaitham and Kaveh can be read in the Mahamata Bulletin Board, Puspa Café Message Board, and the Port Ormos Bulletin Board. 

Hanahaki Disease is a fictional disease in which the victim coughs up flower petals when they suffer from one-sided love. It ends when the beloved returns their feelings (romantic love only; strong friendship is not enough), or when the victim dies. It can be cured through surgical removal, but when the infection is removed, the victim's romantic feelings for their love also disappear.

Please write a piece of fanfiction about Kaveh/Alhaitham, focusing on the Hanahaki trope.

Make a markdown formatted outline, with a numbered list for each chapter and bullet points for each part of what it contains. Do not use ranges for chapters, write them out individually.
'''

StartingPrompt = '''
Title: "Echoes of Eternity"

Prompt:
In the bustling city of Mondstadt, amidst the swirling winds and melodies of freedom, two unlikely souls find themselves drawn together by fate's intricate design. 

Kaeya Alberich, the charismatic Cavalry Captain of the Knights of Favonius, carries secrets as deep as the abyss, hidden beneath his charming facade. Despite his reputation as a flirtatious rogue, his heart is burdened by the weight of his past, leaving him longing for a connection that transcends the shadows.

Meanwhile, Diluc Ragnvindr, the enigmatic owner of the Dawn Winery and Darknight Hero of Mondstadt, is a beacon of strength and resolve, his fiery determination matched only by the flames of his burning vendetta. Yet beneath his stoic demeanor lies a vulnerability born from the loss of family and betrayal, a wound that refuses to heal.

As their paths intertwine amidst the chaos of elemental powers and ancient mysteries, Kaeya and Diluc find themselves entangled in a dance of conflicting emotions. Their rivalry blurs the lines between animosity and attraction, each encounter sparking a wildfire of longing that threatens to consume them both.

Caught between duty and desire, honor and heartache, they must navigate the treacherous waters of their pasts while forging a future fraught with uncertainty. In a world where alliances are tested and betrayals run deep, will they find solace in each other's arms, or will their love be but a fleeting whisper in the winds of time?
'''


# Generate the Outline
Outline = Writer.OutlineGenerator.GenerateOutline(Client, StartingPrompt, Writer.Config.OUTLINE_QUALITY)


Prompt = "Here is an outline that you will use to build your award winning novel from. Remember to spell the character's names correctly.\n\n"
Prompt += Outline
Messages = [Writer.OllamaInterface.BuildUserQuery(Prompt)]


# Detect the number of chapters
Writer.PrintUtils.PrintBanner("Detecting Chapters", "yellow")
NumChapters:int = Writer.ChapterDetector.CountChapters(Writer.OllamaInterface.GetLastMessageText(Messages))
Writer.PrintUtils.PrintBanner(f"Found {NumChapters} Chapter(s)", "yellow")


# Write the chapters
Writer.PrintUtils.PrintBanner("Starting Chapter Writing", "yellow")
StoryBodyText:str = ""
for i in range(1, NumChapters + 1):

    Chapter = Writer.OutlineGenerator.GenerateChapter(Client, i, NumChapters + 1, Outline, Messages, Writer.Config.OUTLINE_QUALITY)

    Messages.append(Writer.OllamaInterface.BuildUserQuery(Chapter))
    StoryBodyText += Chapter + "\n\n\n"
    ChapterWordCount = Writer.Statistics.GetWordCount(Chapter)
    Writer.PrintUtils.PrintBanner(f"Chapter Word Count: {ChapterWordCount}", "blue")



# Calculate Total Words
TotalWords:int = Writer.Statistics.GetWordCount(StoryBodyText)
Writer.PrintUtils.PrintBanner(f"Story Total Word Count: {TotalWords}", "blue")

StatsString:str = "Work Statistics"
StatsString += "Total Words: " + str(TotalWords)


# Now Generate Info
Info = Writer.StoryInfo.GetStoryInfo(Client, Messages)
Title = Info['Title']
Summary = Info['Summary']
Tags = Info['Tags']

print("---------------------------------------------")
print(f"Story Title: {Title}")
print(f"Summary: {Summary}")
print(f"Tags: {Tags}")
print("---------------------------------------------")


# Save The Story To Disk
Writer.PrintUtils.PrintBanner("Saving Story To Disk", "yellow")
FName = f"Stories/Story_{Title.replace(' ', '_')}.md"
with open(FName, "w") as F:
    Out = StatsString + "\n\n\n==============\n\n\n"
    Out += Outline + "\n\n\n==============\n\n\n"
    Out += StoryBodyText
    F.write(Out)
