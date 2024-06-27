#!/bin/bash

cd ..
./Write.py \
-Host 10.1.65.4:11434 \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel ollama/datacrystals/miqulitz120b-v2:latest \
-ChapterOutlineModel ollama/datacrystals/miqulitz120b-v2:latest \
-ChapterS1Model ollama/datacryatals/miqulitz120b-v2:latest \
-ChapterS2Model ollama/datacryatals/miqulitz120b-v2:latest \
-ChapterS3Model ollama/datacryatals/miqulitz120b-v2:latest \
-ChapterS4Model ollama/datacryatals/miqulitz120b-v2:latest \
-ChapterRevisionModel ollama/datacryatals/miqulitz120b-v2:latest \
-RevisionModel llama3:70b \
-EvalModel llama3:70b \
-InfoModel llama3:70b \
-NoScrubChapters \
-Debug

