#!/bin/bash

cd ..
./Write.py \
-Host 10.1.65.4:11434 \
-Seed 999 \
-Prompt Prompts/Genshin/Kaeluc.txt \
-InitialOutlineModel ollama/datacryatals/miqulitz120b-v2:latest \
-ChapterOutlineModel ollama/datacryatals/midnight-rose103b-v2:latest \
-ChapterS1Model ollama/datacryatals/midnight-miqu70b-v1.5:latest \
-ChapterS2Model command-r-plus \
-ChapterS3Model ollama/datacryatals/miqulitz120b-v2:latest \
-ChapterS4Model ollama/datacryatals/midnight-miqu103b-v1:latest \
-ChapterRevisionModel ollama/datacryatals/miqulitz120b-v2:latest \
-RevisionModel llama3:70b \
-EvalModel llama3:70b \
-InfoModel llama3:70b \
-NoScrubChapters \
-Debug \
-NoChapterRevision
