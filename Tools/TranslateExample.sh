#!/bin/bash

cd ..

echo "Running tests with smallest and fastest model"

./Write.py \
-Host localhost:11434 \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel mistral \
-ChapterOutlineModel mistral \
-ChapterS1Model mistral \
-ChapterS2Model mistral \
-ChapterS3Model mistral \
-ChapterS4Model mistral \
-ChapterRevisionModel mistral \
-RevisionModel mistral \
-EvalModel mistral \
-InfoModel mistral \
-CheckerModel mistral \
-NoScrubChapters \
-TranslatorModel mistral \
-Translate "French"

## Note the two additional params:
# -TranslatorModel mistral 
# -Translate "French"