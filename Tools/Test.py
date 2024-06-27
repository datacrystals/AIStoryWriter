#!/bin/python3

import os

print("Developer Testing Utillity.")
print("1 -> Gemini 1.5 flash, llama70b for editing")
print("2 -> Gemini 1.5 flash, Gemini 1.5 flash for editing")
print("3 -> Gemini 1.5 pro, Gemini 1.5 flash for editing")
print("4 -> Gemini 1.5 pro, Gemini 1.5 pro for editing")
print("5 -> mistral:7b, mistral:7b for editing (fast debug test, produces crap output)")
print("6 -> Developer testing script 1, uses many local models, very slow, but decent output")
print("7 -> Developer testing script 2, miqulitz-120b, one model, llama3:70b editor")
print("8 -> Developer testing script 3, miqu-70b-1.5, one model, llama3:70b editor")
print("9 -> Developer testing script 4, gemma2:27b, one model, gemma2:27b editor")

# Get Choice
print("")
choice = input("> ")


# Terrible but effective way to manage the choices
if (choice == "1"):
    os.system('''
cd .. && ./Write.py \
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
              ''')

elif (choice == "2"):
    os.system('''
cd .. && ./Write.py \
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
-RevisionModel google/gemini-1.5-flash \
-EvalModel google/gemini-1.5-flash \
-InfoModel google/gemini-1.5-flash \
-NoScrubChapters \
-Debug
              ''')

elif (choice == "3"):
    os.system('''
cd .. && ./Write.py \
-Host 10.1.65.4:11434 \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel google/gemini-1.5-pro \
-ChapterOutlineModel google/gemini-1.5-pro \
-ChapterS1Model google/gemini-1.5-pro \
-ChapterS2Model google/gemini-1.5-pro \
-ChapterS3Model google/gemini-1.5-pro \
-ChapterS4Model google/gemini-1.5-pro \
-ChapterRevisionModel google/gemini-1.5-flash \
-RevisionModel google/gemini-1.5-flash \
-EvalModel google/gemini-1.5-flash \
-InfoModel google/gemini-1.5-flash \
-NoScrubChapters \
-Debug
              ''')
    
elif (choice == "4"):
    os.system('''
cd .. && ./Write.py \
-Host 10.1.65.4:11434 \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel google/gemini-1.5-pro \
-ChapterOutlineModel google/gemini-1.5-pro \
-ChapterS1Model google/gemini-1.5-pro \
-ChapterS2Model google/gemini-1.5-pro \
-ChapterS3Model google/gemini-1.5-pro \
-ChapterS4Model google/gemini-1.5-pro \
-ChapterRevisionModel google/gemini-1.5-pro \
-RevisionModel google/gemini-1.5-pro \
-EvalModel google/gemini-1.5-pro \
-InfoModel google/gemini-1.5-pro \
-NoScrubChapters \
-Debug
              ''')
    
elif (choice == "5"):
    os.system('''
cd .. && ./Write.py \
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
-NoScrubChapters
              ''')
    
elif (choice == "6"):
    os.system('''
cd .. && ./Write.py \
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
''')
    
elif (choice == "7"):
    os.system('''
cd .. && ./Write.py \
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


''')
    
elif (choice == "8"):
    os.system('''
cd .. && ./Write.py \
-Host 10.1.65.4:11434 \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel ollama/datacryatals/midnight-miqu70b-v1.5:latest \
-ChapterOutlineModel ollama/datacryatals/midnight-miqu70b-v1.5:latest \
-ChapterS1Model ollama/datacryatals/midnight-miqu70b-v1.5:latest \
-ChapterS2Model ollama/datacryatals/midnight-miqu70b-v1.5:latest \
-ChapterS3Model ollama/datacryatals/midnight-miqu70b-v1.5:latest \
-ChapterS4Model ollama/datacryatals/midnight-miqu70b-v1.5:latest \
-ChapterRevisionModel ollama/datacryatals/midnight-miqu70b-v1.5:latest \
-RevisionModel llama3:70b \
-EvalModel llama3:70b \
-InfoModel llama3:70b \
-NoScrubChapters \
-Debug

''')

    
elif (choice == "9"):
    os.system('''
cd .. && ./Write.py \
-Host 10.1.65.4:11434 \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel gemma2:27b \
-ChapterOutlineModel gemma2:27b \
-ChapterS1Model gemma2:27b \
-ChapterS2Model gemma2:27b \
-ChapterS3Model gemma2:27b \
-ChapterS4Model gemma2:27b \
-ChapterRevisionModel gemma2:27b \
-RevisionModel gemma2:27b \
-EvalModel gemma2:27b \
-InfoModel gemma2:27b \
-NoScrubChapters \
-Debug

''')