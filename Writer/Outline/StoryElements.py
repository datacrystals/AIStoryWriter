import Writer.LLMEditor
import Writer.PrintUtils
import Writer.Config


def GenerateStoryElements(Interface, _Logger, _OutlinePrompt):

    Prompt: str = f"""
I'm working on writing a fictional story, and I'd like your help writing out the story elements.

Here's the prompt for my story.
<PROMPT>
{_OutlinePrompt}
</PROMPT>

Please make your response have the following format:

<RESPONSE_TEMPLATE>
# Story Title

## Genre
- **Category**: (e.g., romance, mystery, science fiction, fantasy, horror)

## Theme
- **Central Idea or Message**:

## Pacing
- **Speed**: (e.g., slow, fast)

## Style
- **Language Use**: (e.g., sentence structure, vocabulary, tone, figurative language)

## Plot
- **Exposition**:
- **Rising Action**:
- **Climax**:
- **Falling Action**:
- **Resolution**:

## Setting
### Setting 1
- **Time**: (e.g., present day, future, past)
- **Location**: (e.g., city, countryside, another planet)
- **Culture**: (e.g., modern, medieval, alien)
- **Mood**: (e.g., gloomy, high-tech, dystopian)

(Repeat the above structure for additional settings)

## Conflict
- **Type**: (e.g., internal, external)
- **Description**:

## Symbolism
### Symbol 1
- **Symbol**:
- **Meaning**:

(Repeat the above structure for additional symbols)

## Characters
### Main Character(s)
#### Main Character 1
- **Name**:
- **Physical Description**:
- **Personality**:
- **Background**:
- **Motivation**:

(Repeat the above structure for additional main characters)


### Supporting Characters
#### Character 1
- **Name**:
- **Physical Description**:
- **Personality**:
- **Background**:
- **Role in the story**:

#### Character 2
- **Name**:
- **Physical Description**:
- **Personality**:
- **Background**:
- **Role in the story**:

#### Character 3
- **Name**:
- **Physical Description**:
- **Personality**:
- **Background**:
- **Role in the story**:

#### Character 4
- **Name**:
- **Physical Description**:
- **Personality**:
- **Background**:
- **Role in the story**:

#### Character 5
- **Name**:
- **Physical Description**:
- **Personality**:
- **Background**:
- **Role in the story**:

#### Character 6
- **Name**:
- **Physical Description**:
- **Personality**:
- **Background**:
- **Role in the story**:

#### Character 7
- **Name**:
- **Physical Description**:
- **Personality**:
- **Background**:
- **Role in the story**:

#### Character 8
- **Name**:
- **Physical Description**:
- **Personality**:
- **Background**:
- **Role in the story**:

(Repeat the above structure for additional supporting character)

</RESPONSE_TEMPLATE>

Of course, don't include the XML tags - those are just to indicate the example.
Also, the items in parenthesis are just to give you a better idea of what to write about, and should also be omitted from your response.
    
    """

    # Generate Initial Story Elements
    _Logger.Log(f"Generating Main Story Elements", 4)
    Messages = [Interface.BuildUserQuery(Prompt)]
    Messages = Interface.SafeGenerateText(
        _Logger, Messages, Writer.Config.INITIAL_OUTLINE_WRITER_MODEL, _MinWordCount=300
    )
    Elements: str = Interface.GetLastMessageText(Messages)
    _Logger.Log(f"Done Generating Main Story Elements", 4)

    return Elements
