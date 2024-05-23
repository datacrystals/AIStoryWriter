#!/bin/python3
import os

# User Config Options
PROMPT = "Prompts/SL/Hacking2.txt"
SEED = 999
HOST = "10.1.65.4:11434"
OUTPUT_DIR = "Stories/BatchTesting"
INITIAL_OUTLINE_MODELS = ["datacrystals/Midnight-Rose-103B-v2:latest", "datacrystals/miquliz-120b-v2.0.Q4_K_M.gguf:latest", "datacrystals/WizardLM-2-8x22B-Q3_K_M:latest"]
CHAPTER_OUTLINE_MODELS = ["datacrystals/Midnight-Rose-103B-v2:latest", "datacrystals/miquliz-120b-v2.0.Q4_K_M.gguf:latest", "datacrystals/WizardLM-2-8x22B-Q3_K_M:latest"]
CHAPTER_MODELS = ["datacrystals/Midnight-Rose-103B-v2:latest", "datacrystals/miquliz-120b-v2.0.Q4_K_M.gguf:latest", "datacrystals/WizardLM-2-8x22B-Q3_K_M:latest"]
REVISION_MODELS = ["llama3:70b"]
EVAL_MODELS = ["llama3:70b"]
SCRUB_MODELS = ["llama3:70b", "datacrystals/WizardLM-2-8x22B-Q3_K_M:latest"]
OUTLINE_MIN_REVISION_VALS = [0, 1]
OUTLINE_MAX_REVISION_VALS = [3]
CHAPTER_MIN_REVISION_VALS = [0]
CHAPTER_MAX_REVISION_VALS = [3]



# This system allows for systematic story generation with different prompts, so we can get an idea of what works and what doesn't.
print("Starting Systematic Writing Testing")

# Generate System Calls
StoryIndex:int = 0
SystemCalls:list = []
for InitialOutlineModel in INITIAL_OUTLINE_MODELS:
    for ChapterOutlineModel in CHAPTER_OUTLINE_MODELS:
        for ChapterModel in CHAPTER_MODELS:
            for RevisionModel in REVISION_MODELS:
                for EvalModel in EVAL_MODELS:
                    for ScrubModel in SCRUB_MODELS:
                        for OutlineMinRevision in OUTLINE_MIN_REVISION_VALS:
                            for OutlineMaxRevision in OUTLINE_MAX_REVISION_VALS:
                                for ChapterMinRevision in CHAPTER_MIN_REVISION_VALS:
                                    for ChapterMaxRevision in CHAPTER_MAX_REVISION_VALS:

                                        SystemCall:str = f"./Write.py -Prompt {PROMPT} -Host {HOST} -Seed {SEED} -Output {OUTPUT_DIR + '/' + str(StoryIndex) + '.md'} -InitialOutlineModel {InitialOutlineModel} -ChapterOutlineModel {ChapterOutlineModel} -ChapterModel {ChapterModel} -RevisionModel {RevisionModel} -EvalModel {EvalModel} -ScrubModel {ScrubModel} -OutlineMinRevisions {OutlineMinRevision} -OutlineMaxRevisions {OutlineMaxRevision} -ChapterMinRevisions {ChapterMinRevision} -ChapterMaxRevisions {ChapterMaxRevision}"
                                        SystemCalls.append(SystemCall)
                                        StoryIndex += 1


# Write index of all system calls, so we can keep track of what story corresponds to what prompt
Index:str = "# Prompt/File Index  "
for i in range(len(SystemCalls)):
    Index += f"- \"{str(StoryIndex) + '.md'}\": \"{SystemCalls[i]}\"  \n"

with open(f"{OUTPUT_DIR}/Index.md", "w") as f:
    f.write(Index)


# Now, run each of the system prompts
print(f" - Running System Prompts Now, This Will Likely Take A *LONG* Time.")
for i in range(len(SystemCalls)):
    print(f"    - Running System Call {i}/{}")