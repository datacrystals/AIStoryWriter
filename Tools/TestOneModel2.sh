#!/bin/bash

cd ..
./Write.py \
-Host 10.1.65.4:11434 \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel datacrystals/midnight-miqu70b-v1.5:latest \
-ChapterOutlineModel datacrystals/midnight-miqu70b-v1.5:latest \
-ChapterS1Model datacrystals/midnight-miqu70b-v1.5:latest \
-ChapterS2Model datacrystals/midnight-miqu70b-v1.5:latest \
-ChapterS3Model datacrystals/midnight-miqu70b-v1.5:latest \
-ChapterS4Model datacrystals/midnight-miqu70b-v1.5:latest \
-ChapterRevisionModel datacrystals/midnight-miqu70b-v1.5:latest \
-RevisionModel llama3:70b \
-EvalModel llama3:70b \
-InfoModel llama3:70b \
-NoScrubChapters \
-Debug

