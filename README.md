# AI Story Generatior

This project aims to be a LLM-based story generator which produces medium to full-length novels based on a user-provided prompt.

So far, it's a work in progress, as I'm still focusing on getting the bugs worked out and improving the generated output quality.


## Note about usage

This system will generate a story based on a user provided prompt. Simply create a file with your intended prompt in a text file, and pass the path to that as a parameter (use ./Write.py --help) to get a full list of parameters.



## Installation

Installing is pretty easy - just clone this repo, install [OLLAMA](https://ollama.com/) on some machine you have, and point the writer at it. 

For now, you also have to download the different LLMs that this project uses manually (sorry). Please see some of the test scripts for an idea of the models that I've been using so far.
The project uses a few different LLMs to generate different parts of the output (for example one for outline generation, another for each stage for the chapter generation, etc.), so make sure you have a few hundred GB of disk space free for this.

I've been developing on a machine with 3x NVIDIA TESLA P40 24GB GPUs, so all the models used by default (and in the testing scripts), are 70 billion parameters and up. I've not thoroughly experimented with smaller models as of yet - those likely aren't going to produce as good of a result, but they will definitely be much faster to run.
