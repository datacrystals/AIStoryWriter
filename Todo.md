# shit list of things to fix

 - Implement chapter length prompting (autodetect number of chapters, and how long they should be to match the target)
 - tagging system (use tags in the initial prompt)
 - optional base summmary to guide the AI
 - Implement ai feedback system
    - at the end of the story, feed it into a fresh llama context
        - is the story complete?
        - is the story well written?
        - general feedback
    - then have it take that feedback and edit accordingly

- that can also be done per-chapter
    - so at the end of each chapter, have the AI check itself
    - is that chapter the right length
        - if not, ask it to retry but add more info until it's at the word count
        - once at the wordcount, remove old

- prompt llm for initial outline
- then have it revise its initial outline
- have it then add detail and revise some more
- maybe repeat that a few times

- then when ready, have the llm get the outline for each chapter, and separate it

- then remind the llm when writing each chapter what the outline is for that chapter

- have it summarize the other chapters as needed to make the context length managble