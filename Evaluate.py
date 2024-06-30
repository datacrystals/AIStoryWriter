#!/bin/python3

import argparse
import time
import datetime
import os

import Writer.Interface.Wrapper
import Writer.Config
import Writer.PrintUtils


# Setup Argparser
Parser = argparse.ArgumentParser()
Parser.add_argument("-Story", help="Path to file containing the story to evaluate")
Parser.add_argument("-Output", default="", type=str, help="Optional file output path, if none is specified, we will only print the rating to terminal",)
Parser.add_argument("-Host", default="localhost:11434", type=str, help="HTTP URL to OLLAMA instance",)
Parser.add_argument("-Model", default="llama3:70b", type=str, help="Model to use for writing the base outline content",)

Args = Parser.parse_args()

Writer.Config.OLLAMA_HOST = Args.Host


# Measure Generation Time
StartTime_s = time.time()

# Setup Logger
Logger = Writer.PrintUtils.Logger("EvalLogs")

# Load the initial story
Story:str = ""
with open(Args.Story, "r") as f:
    Story = f.read()

Interface = Writer.Interface.Wrapper.Interface([Args.Model])
Messages = [Interface.BuildSystemQuery("You are a helpful AI language model.")]
Messages.append(Interface.BuildUserQuery(f"""
Please rate the below story:
                                          
<STORY>
{Story}
</STORY>

Please make your story have 
"""))
Messages = Interface.ChatAndStreamResponse(Logger, Messages, Args.Model)


# Calculate Eval Time
EndTime_s = time.time()
TotalEvalTime_s = round(EndTime_s - StartTime_s)



# Build Report
Report:str = ""

# Optionally write Report To Disk
if (Args.Output != ""):
    with open(Args.Output, "w") as f:
        f.write(Report)





