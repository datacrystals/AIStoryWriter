#!/bin/bash

cd ..
./Write.py \
-Host 10.1.65.4:11434 \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel google/gemini-1.5-flash \
-ChapterOutlineModel google/gemini-1.5-flash \
-ChapterS1Model google/gemini-1.5-flash \
-ChapterS2Model google/gemini-1.5-flash \
-ChapterS3Model google/gemini-1.5-flash \
-ChapterS4Model google/gemini-1.5-flash \
-ChapterRevisionModel google/gemini-1.5-flash \
-RevisionModel ollama/llama3:70b \
-EvalModel ollama/llama3:70b \
-InfoModel ollama/llama3:70b \
-NoScrubChapters \
-Debug

