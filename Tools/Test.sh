#!/bin/bash

cd ..
./Write.py \
-Host 10.1.65.4:11434 \
-Seed 999 \
-Prompt ExamplePrompts/Example1.txt \
-InitialOutlineModel datacrystals/miqulitz120b-v2:latest \
-ChapterOutlineModel datacrystals/midnight-rose103b-v2:latest \
-ChapterS1Model datacrystals/midnight-miqu70b-v1.5:latest \
-ChapterS2Model command-r-plus \
-ChapterS3Model datacrystals/miqulitz120b-v2:latest \
-ChapterS4Model datacrystals/midnight-miqu103b-v1:latest \
-ChapterRevisionModel datacrystals/miqulitz120b-v2:latest \
-RevisionModel llama3:70b \
-EvalModel llama3:70b \
-InfoModel llama3:70b \
-NoScrubChapters \
-Debug

