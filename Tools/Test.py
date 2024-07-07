#!/bin/python3

import os

print("Developer Testing Utility.")

# Get Choice For Model
print("Chose Model: ")
print("-------------------------------------------")
print("1 -> Gemini 1.5 flash, llama70b for editing")
print("2 -> Gemini 1.5 flash, Gemini 1.5 flash for editing")
print("3 -> Gemini 1.5 pro, Gemini 1.5 flash for editing")
print("4 -> Gemini 1.5 pro, Gemini 1.5 pro for editing")
print("5 -> ollama://mistral:7b, ollama://mistral:7b for editing (fast debug test, produces crap output)")
print("6 -> Developer testing script 1, uses many local models, very slow, but decent output")
print("7 -> Developer testing script 2, miqulitz-120b, one model, llama3:70b editor")
print("8 -> Developer testing script 3, miqu-70b-1.5, one model, llama3:70b editor")
print("9 -> Developer testing script 4, gemma2:27b, one model, gemma2:27b editor")
print("10 -> Developer testing script 4, qwen2:72b, one model, qwen2:72b editor")
print("11 -> Developer testing script 5, llama3, one model, llama3 editor")
print("12 -> Developer testing script 6, gemma, one model, gemma editor")
print("-------------------------------------------")


# Get Choice
print("")
choice = input("> ")

# Get Choice For Prompt
print("Chose Prompt:")
print("-------------------------------------------")
print("1 -> ExamplePrompts/Example1/Prompt.txt")
print("2 -> ExamplePrompts/Example2/Prompt.txt")
print("3 -> Custom Prompt")
print("-------------------------------------------")
print("Default = 1")
print("")
PromptChoice = input("> ")

Prompt = ""
if (PromptChoice == "" or PromptChoice == "1"):
    Prompt = "ExamplePrompts/Example1/Prompt.txt"
elif (PromptChoice == "2"):
    Prompt = "ExamplePrompts/Example2/Prompt.txt"
elif (PromptChoice == "3"):
    Prompt = input("Enter Prompt File Path: ")



# Now, Add Any Extra Flags
print("Extra Flags:")
# print("-------------------------------------------")
# print("1 -> ExamplePrompts/Example1/Prompt.txt")
# print("2 -> ExamplePrompts/Example2/Prompt.txt")
# print("3 -> Custom Prompt")
# print("-------------------------------------------")
print("Default = ''")
print("")
ExtraFlags = input("> ")





# Terrible but effective way to manage the choices
if (choice == "1"):
    os.system(f'''
cd .. && ./Write.py \
-Seed 999 \
-Prompt {Prompt} \
-InitialOutlineModel google://gemini-1.5-flash \
-ChapterOutlineModel google://gemini-1.5-flash \
-ChapterS1Model google://gemini-1.5-flash \
-ChapterS2Model google://gemini-1.5-flash \
-ChapterS3Model google://gemini-1.5-flash \
-ChapterS4Model google://gemini-1.5-flash \
-ChapterRevisionModel google://gemini-1.5-flash \
-RevisionModel ollama://llama3:70b@10.1.65.4:11434 \
-EvalModel ollama://llama3:70b@10.1.65.4:11434 \
-InfoModel ollama://llama3:70b@10.1.65.4:11434 \
-NoScrubChapters \
-Debug {ExtraFlags}
              ''')

elif (choice == "2"):
    os.system(f'''
cd .. && ./Write.py \
-Seed 999 \
-Prompt {Prompt} \
-InitialOutlineModel google://gemini-1.5-flash \
-ChapterOutlineModel google://gemini-1.5-flash \
-ChapterS1Model google://gemini-1.5-flash \
-ChapterS2Model google://gemini-1.5-flash \
-ChapterS3Model google://gemini-1.5-flash \
-ChapterS4Model google://gemini-1.5-flash \
-ChapterRevisionModel google://gemini-1.5-flash \
-RevisionModel google://gemini-1.5-flash \
-EvalModel google://gemini-1.5-flash \
-InfoModel google://gemini-1.5-flash \
-NoScrubChapters \
-Debug {ExtraFlags}
              ''')

elif (choice == "3"):
    os.system(f'''
cd .. && ./Write.py \
-Seed 999 \
-Prompt {Prompt} \
-InitialOutlineModel google://gemini-1.5-pro \
-ChapterOutlineModel google://gemini-1.5-pro \
-ChapterS1Model google://gemini-1.5-pro \
-ChapterS2Model google://gemini-1.5-pro \
-ChapterS3Model google://gemini-1.5-pro \
-ChapterS4Model google://gemini-1.5-pro \
-ChapterRevisionModel google://gemini-1.5-flash \
-RevisionModel google://gemini-1.5-flash \
-EvalModel google://gemini-1.5-flash \
-InfoModel google://gemini-1.5-flash \
-NoScrubChapters \
-Debug {ExtraFlags}
              ''')
    
elif (choice == "4"):
    os.system(f'''
cd .. && ./Write.py \
-Seed 999 \
-Prompt {Prompt} \
-InitialOutlineModel google://gemini-1.5-pro \
-ChapterOutlineModel google://gemini-1.5-pro \
-ChapterS1Model google://gemini-1.5-pro \
-ChapterS2Model google://gemini-1.5-pro \
-ChapterS3Model google://gemini-1.5-pro \
-ChapterS4Model google://gemini-1.5-pro \
-ChapterRevisionModel google://gemini-1.5-pro \
-RevisionModel google://gemini-1.5-pro \
-EvalModel google://gemini-1.5-pro \
-InfoModel google://gemini-1.5-pro \
-NoScrubChapters \
-Debug {ExtraFlags}
              ''')
    
elif (choice == "5"):
    os.system(f'''
cd .. && ./Write.py \
-Seed 999 \
-Prompt {Prompt} \
-InitialOutlineModel ollama://mistral \
-ChapterOutlineModel ollama://mistral \
-ChapterS1Model ollama://mistral \
-ChapterS2Model ollama://mistral \
-ChapterS3Model ollama://mistral \
-ChapterS4Model ollama://mistral \
-ChapterRevisionModel ollama://mistral \
-RevisionModel ollama://mistral \
-EvalModel ollama://mistral \
-InfoModel ollama://mistral \
-CheckerModel ollama://mistral \
-NoScrubChapters {ExtraFlags}
              ''')
    
elif (choice == "6"):
    os.system(f'''
cd .. && ./Write.py \
-Seed 999 \
-Prompt Prompts/Genshin/Kaeluc.txt \
-InitialOutlineModel ollama://datacrystals/miqulitz120b-v2:latest@10.1.65.4:11434 \
-ChapterOutlineModel ollama://datacrystals/midnight-rose103b-v2:latest@10.1.65.4:11434 \
-ChapterS1Model ollama://datacrystals/midnight-miqu70b-v1.5:latest@10.1.65.4:11434 \
-ChapterS2Model ollama://command-r-plus@10.1.65.4:11434 \
-ChapterS3Model ollama://datacrystals/miqulitz120b-v2:latest@10.1.65.4:11434 \
-ChapterS4Model ollama://datacrystals/midnight-miqu103b-v1:latest@10.1.65.4:11434 \
-ChapterRevisionModel ollama://datacrystals/miqulitz120b-v2:latest@10.1.65.4:11434 \
-RevisionModel ollama://llama3:70b@10.1.65.4:11434 \
-EvalModel ollama://llama3:70b@10.1.65.4:11434 \
-InfoModel ollama://llama3:70b@10.1.65.4:11434 \
-NoScrubChapters \
-Debug \
-NoChapterRevision {ExtraFlags}
''')
    
elif (choice == "7"):
    os.system(f'''
cd .. && ./Write.py \
-Seed 999 \
-Prompt {Prompt} \
-InitialOutlineModel ollama://datacrystals/miqulitz120b-v2:latest@10.1.65.4:11434 \
-ChapterOutlineModel ollama://datacrystals/miqulitz120b-v2:latest@10.1.65.4:11434 \
-ChapterS1Model ollama://datacrystals/miqulitz120b-v2:latest@10.1.65.4:11434 \
-ChapterS2Model ollama://datacrystals/miqulitz120b-v2:latest@10.1.65.4:11434 \
-ChapterS3Model ollama://datacrystals/miqulitz120b-v2:latest@10.1.65.4:11434 \
-ChapterS4Model ollama://datacrystals/miqulitz120b-v2:latest@10.1.65.4:11434 \
-ChapterRevisionModel ollama://datacrystals/miqulitz120b-v2:latest@10.1.65.4:11434 \
-RevisionModel ollama://llama3:70b@10.1.65.4:11434 \
-EvalModel ollama://llama3:70b@10.1.65.4:11434 \
-InfoModel ollama://llama3:70b@10.1.65.4:11434 \
-NoScrubChapters \
-Debug {ExtraFlags}


''')
    
elif (choice == "8"):
    os.system(f'''
cd .. && ./Write.py \
-Seed 999 \
-Prompt {Prompt} \
-InitialOutlineModel ollama://datacrystals/midnight-miqu70b-v1.5:latest@10.1.65.4:11434 \
-ChapterOutlineModel ollama://datacrystals/midnight-miqu70b-v1.5:latest@10.1.65.4:11434 \
-ChapterS1Model ollama://datacrystals/midnight-miqu70b-v1.5:latest@10.1.65.4:11434 \
-ChapterS2Model ollama://datacrystals/midnight-miqu70b-v1.5:latest@10.1.65.4:11434 \
-ChapterS3Model ollama://datacrystals/midnight-miqu70b-v1.5:latest@10.1.65.4:11434 \
-ChapterS4Model ollama://datacrystals/midnight-miqu70b-v1.5:latest@10.1.65.4:11434 \
-ChapterRevisionModel ollama://datacrystals/midnight-miqu70b-v1.5:latest@10.1.65.4:11434 \
-RevisionModel ollama://llama3:70b@10.1.65.4:11434 \
-EvalModel ollama://llama3:70b@10.1.65.4:11434 \
-InfoModel ollama://llama3:70b@10.1.65.4:11434 \
-NoScrubChapters \
-Debug {ExtraFlags}

''')

    
elif (choice == "9"):
    os.system(f'''
cd .. && ./Write.py \
-Seed 999 \
-Prompt {Prompt} \
-InitialOutlineModel ollama://gemma2:27b@10.1.65.4:11434 \
-ChapterOutlineModel ollama://gemma2:27b@10.1.65.4:11434 \
-ChapterS1Model ollama://gemma2:27b@10.1.65.4:11434 \
-ChapterS2Model ollama://gemma2:27b@10.1.65.4:11434 \
-ChapterS3Model ollama://gemma2:27b@10.1.65.4:11434 \
-ChapterS4Model ollama://gemma2:27b@10.1.65.4:11434 \
-ChapterRevisionModel ollama://gemma2:27b@10.1.65.4:11434 \
-RevisionModel ollama://gemma2:27b@10.1.65.4:11434 \
-EvalModel ollama://gemma2:27b@10.1.65.4:11434 \
-InfoModel ollama://gemma2:27b@10.1.65.4:11434 \
-NoScrubChapters \
-Debug {ExtraFlags}

''')
    
elif (choice == "10"):
    os.system('''
cd .. && ./Write.py \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel ollama://qwen2:72b@10.1.65.4:11434 \
-ChapterOutlineModel ollama://qwen2:72b@10.1.65.4:11434 \
-ChapterS1Model ollama://qwen2:72b@10.1.65.4:11434 \
-ChapterS2Model ollama://qwen2:72b@10.1.65.4:11434 \
-ChapterS3Model ollama://qwen2:72b@10.1.65.4:11434 \
-ChapterS4Model ollama://qwen2:72b@10.1.65.4:11434 \
-ChapterRevisionModel ollama://qwen2:72b@10.1.65.4:11434 \
-RevisionModel ollama://qwen2:72b@10.1.65.4:11434 \
-EvalModel ollama://qwen2:72b@10.1.65.4:11434 \
-InfoModel ollama://qwen2:72b@10.1.65.4:11434 \
-NoScrubChapters \
-Debug {ExtraFlags}

''')
    
elif (choice == "11"):
    os.system('''
cd .. && ./Write.py \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel ollama://llama3@10.1.65.4:11434 \
-ChapterOutlineModel ollama://llama3@10.1.65.4:11434 \
-ChapterS1Model ollama://llama3@10.1.65.4:11434 \
-ChapterS2Model ollama://llama3@10.1.65.4:11434 \
-ChapterS3Model ollama://llama3@10.1.65.4:11434 \
-ChapterS4Model ollama://llama3@10.1.65.4:11434 \
-ChapterRevisionModel ollama://llama3@10.1.65.4:11434 \
-RevisionModel ollama://llama3@10.1.65.4:11434 \
-EvalModel ollama://llama3@10.1.65.4:11434 \
-InfoModel ollama://llama3@10.1.65.4:11434 \
-NoScrubChapters \
-Debug {ExtraFlags}

''')
    
elif (choice == "12"):
    os.system('''
cd .. && ./Write.py \
-Seed 999 \
-Prompt ExamplePrompts/Example1/Prompt.txt \
-InitialOutlineModel ollama://gemma@10.1.65.4:11434 \
-ChapterOutlineModel ollama://gemma@10.1.65.4:11434 \
-ChapterS1Model ollama://gemma@10.1.65.4:11434 \
-ChapterS2Model ollama://gemma@10.1.65.4:11434 \
-ChapterS3Model ollama://gemma@10.1.65.4:11434 \
-ChapterS4Model ollama://gemma@10.1.65.4:11434 \
-ChapterRevisionModel ollama://gemma@10.1.65.4:11434 \
-RevisionModel ollama://gemma@10.1.65.4:11434 \
-EvalModel ollama://gemma@10.1.65.4:11434 \
-InfoModel ollama://gemma@10.1.65.4:11434 \
-NoScrubChapters \
-Debug {ExtraFlags}

''')