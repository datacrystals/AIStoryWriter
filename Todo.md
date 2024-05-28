
- have it summarize the other chapters as needed to make the context length managble


-- NEW IDEAS FROM 2024-05-16

    maybe then prompt it to add dialogue to it's chapter, and correct the pace of the chapter? idk
    - perhaps after generating each chapter, have it summarize it then update the outline according to the chapter summary to maintain coherance better.


# potentially have it update the outline after writing each chapter, that way it can be flexible and change as it starts to write it
# have it check if the whole story follows the outline at the end and suggest edits of the entire thing rather than chapter by chapter

make use of system prompts!!

Make the chapter outline and content generator aware of the total num chapters
that way, it knows not to write itself into a corner, and to actually follow the bloody outline.


## Fixlist

REMEMBER TO TELL THE STUPID LLM, NOT TO JUST ANSWER THE QUESTIONS, THAT'S NOT WHAT WE MEAN!!!!!
Perhaps do that via some message like this: `Don't answer these questions directly, instead make your writing implicitly answer them. (Show, don't tell)`

- Iterative generation (do that chapter-by-chapter)

    - Firstly, we've generated the story focusing on plot pretty much exclusively (done)
        - Pacing: Is the story rushing over certain plot points and excessively focusing on others?
        - Details: How are things described? Is it repetitive? Is the word choice appropriate for the scene? Are we describing things too much or too little?
        - Flow: Does each chapter flow into the next? Does the plot make logical sense to the reader? Does it have a specific narrative structure at play? Is the narrative structure consistent throughout the story?
        - Genre: What is the genre? What language is appropriate for that genre? Do the scenes support the genre?
        - Characters: Are there enough characters? Too many? Do the names make sense in the setting? What are their motives, and do they make sense?

    - Next, we need to have it add character development
        - Characters: Who are the characters in this chapter? What do they mean to each other? What is the situation between them? Is it a conflict? Is there tension? Is there a reason that the characters have been brought together?
        - Development:  What are the goals of each character, and do they meet those goals? Do the characters change and exhibit growth? Do the goals of each character change over the story?

    - Then, iterate and add dialogue 
        - Dialogue: Does the dialogue make sense? Is it appropriate given the situation? Does the pacing make sense for the scene E.g: (Is it fast-paced because they're running, or slow-paced because they're having a romantic dinner)? 
        - Disruptions: If the flow of dialogue is disrupted, what is the reason for that disruption? Is it a sense of urgency? What is causing the disruption? How does it affect the dialogue moving forwards? 
    
    - Final edit pass?
        Make sure to double check the following:
            - Pacing
            - Flow
            - Details
            - Characters
            - Development
            - Genre
            - Disruptions/conflict

So process wise:

for chapter in chapters:

    Generate plot
    then add char development
    then add dialogue
    then final pass
    
    finally do the criteria checking
    and revise all at once

# Maybe put in definitions for the terms used if that's a problem

# TRY REPLACING --- with ``` FORMATTING
# check for nested ``` blocks, by having a helper function that removes them prior to wrapping it in a nested set of ``` blocks

give the chapter generators the outline every time
make sure they also keep the text so it flows between chapters
tell them to read the previous chapters andm ensure that their writing flows from each chapter to the next one so it's not a disjointed piece of crap


--

# iterative generation idea

Generate the story - then create an outline chpater by chapter
then add detail to the outline
generate it all again?
