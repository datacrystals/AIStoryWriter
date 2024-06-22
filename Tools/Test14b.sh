#!/bin/bash

cd ..

echo "Running tests with smaller models (~14b params, rather than the normal 70b param models)"

./Write.py \
-Host localhost:11434 \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel phi3:14b \
-ChapterOutlineModel phi3:14b \
-ChapterS1Model aya:8b \
-ChapterS2Model phi3:14b \
-ChapterS3Model aya:8b \
-ChapterS4Model llava:13b \
-ChapterRevisionModel phi3:14b \
-RevisionModel llama3 \
-EvalModel llama3 \
-InfoModel llama3 \
-NoScrubChapters \
-Debug