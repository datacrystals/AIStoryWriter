#!/bin/bash
cd ..
./Write.py -Host 10.1.65.4:11434 -Seed 999 -Prompt Prompts/SL/Hacking2.txt -InitialOutlineModel datacrystals/Miqulitz120B-V2:latest -ChapterOutlineModel datacrystals/MidnightRose103B-V2:latest -ChapterS1Model datacrystals/MidnightMiqu70B-V1.5:latest -ChapterS2Model command-r-plus -ChapterS3Model datacrystals/Miqulitz120B-V2:latest -ChapterS4Model datacrystals/MidnightMiqu103B-V1:latest -ChapterRevisionModel datacrystals/Miqulitz120B-V2:latest -RevisionModel llama3:70b -EvalModel llama3:70b -InfoModel llama3:70b -NoScrubChapters
