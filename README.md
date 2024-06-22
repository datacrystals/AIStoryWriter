# AI Story Generatior

This project aims to be a LLM-based story generator which produces medium to full-length novels based on a user-provided prompt.

So far, it's a work in progress, as I'm still focusing on getting the bugs worked out and improving the generated output quality.

Here's what the (mostly up-to-date) process looks like as a block diagram. I'll try to keep this up-to-date but no promises.

![Block Diagram](Docs/BlockDiagram.drawio.svg)



## Functionality 
Here's what the system does well, and what it has limitations doing.

### What works well
- Length - usually the system will generate a decent length story, although this has been shorter recently. Should be easy to fix though, as you can specify the num chapters you want in your prompt.
- Characters - most of the time, the LLMs will understand what character is what and write appropriately.
- Outlines - for the most part, the outlines the system generates are actually pretty good, and seem very interesting. If nothing else, this project generates good outlines.

### What doesn't work well
- Tends to use a few token phrases "the tension was palpable", etc. More of an LLM issue though.
- System sometimes writes chapters that don't flow together - they tend to feel disjointed. This has been my current area of focus, and they feel at least somewhat connected now (at least initially).
- Pacing issues - frequently the language models don't understand what to focus their writing on, and often skip over the juicy parts of a story.
- Generation speed is slow, at least on my limited hardware - this leads to 5+ hour generation times, making debugging tricky.

## Examples

Here's an example as of 2024-06-21 - note that there are still some major issues that I'm working on fixing (see limitations section).

- [Prompt](ExamplePrompts/Example1/Prompt.txt)
- [Output (2024-06-20 Version)](ExamplePrompts/Example1/Output_2024-06-20.md)

I've made some changes since this version, and I'm regenerating the example, so this is a bit outdated.


Again, please note that this is still a WIP, so there's still quite a bit to fix here. 




## Usage

This system will generate a story based on a user provided prompt. Simply create a file with your intended prompt in a text file, and pass the path to that as a parameter (use ./Write.py --help) to get a full list of parameters.

As of 2024-06-22, here's an example usage command, but make sure to check for any updated test scripts as those will be more up-to-date than this readme.

Make sure to substitute in values for your OLLAMA host.


### 72GiB VRAM
If you have 72GiB or more of VRAM, this example should work for you.

Note that you'll need to download all of the used models via `ollama pull [modelname]` on your OLLAMA host.

```sh

./Write.py \
-Host [OLLAMA HOST HERE]:11434 \
-Seed 1234 \
-Prompt ExamplePrompts/Example1/Prompt.txt  \
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
-NoScrubChapters

```

### 20GiB VRAM
Alternatively, this example should work for you if you have about 20GiB VRAM. Again, you'll need to download these models. I haven't tested this one nearly as much as the 72GiB version. If someone wants to experiment with different models and let me know what works best, I'd be thrilled.

```sh

./Write.py \
-Host [OLLAMA HOST HERE]:11434 \
-Seed 1234 \
-Prompt ExamplePrompts/Example1/Prompt.txt  \
-InitialOutlineModel phi3:14b \
-ChapterOutlineModel phi3:14b \
-ChapterS1Model aya:8b \
-ChapterS2Model phi3:14b \
-ChapterS3Model aya:8b \
-ChapterS4Model llava:13b \
-ChapterRevisionModel phi3:14b \
-RevisionModel llama3 \
-EvalModel llama3 \
-InfoModel llama3 \
-NoScrubChapters
```

### Translating

This project supports translating the generated story into another language via the `-Translate` argument. Simply specify a language after the flag: `-Translate "French"`.

If you want to use a specific model for translation, use the -TranslatorModel flag: `-TranslatorModel llama3:70b`

Very simple example [here](ExamplePrompts/ShortDebuggingStory/TranslationExample.md) (note the story prompt here was intended to be as short as possible for fast debugging).


### Command Line Flags

Here's a full list of arguments as of 2024-06-22:

```
usage: Write.py [-h] [-Prompt PROMPT] [-Output OUTPUT] [-Host HOST] [-InitialOutlineModel INITIALOUTLINEMODEL] [-ChapterOutlineModel CHAPTEROUTLINEMODEL] [-ChapterS1Model CHAPTERS1MODEL] [-ChapterS2Model CHAPTERS2MODEL]
                [-ChapterS3Model CHAPTERS3MODEL] [-ChapterS4Model CHAPTERS4MODEL] [-ChapterRevisionModel CHAPTERREVISIONMODEL] [-RevisionModel REVISIONMODEL] [-EvalModel EVALMODEL] [-InfoModel INFOMODEL] [-ScrubModel SCRUBMODEL]
                [-CheckerModel CHECKERMODEL] [-TranslatorModel TRANSLATORMODEL] [-Translate TRANSLATE] [-Seed SEED] [-OutlineMinRevisions OUTLINEMINREVISIONS] [-OutlineMaxRevisions OUTLINEMAXREVISIONS]
                [-ChapterMinRevisions CHAPTERMINREVISIONS] [-ChapterMaxRevisions CHAPTERMAXREVISIONS] [-NoChapterRevision] [-NoScrubChapters] [-ExpandOutline] [-EnableFinalEditPass] [-Debug]

options:
  -h, --help            show this help message and exit
  -Prompt PROMPT        Path to file containing the prompt
  -Output OUTPUT        Optional file output path, if none is speciifed, we will autogenerate a file name based on the story title
  -Host HOST            HTTP URL to ollama instance
  -InitialOutlineModel INITIALOUTLINEMODEL
                        Model to use for writing the base outline content
  -ChapterOutlineModel CHAPTEROUTLINEMODEL
                        Model to use for writing the per-chapter outline content
  -ChapterS1Model CHAPTERS1MODEL
                        Model to use for writing the chapter (stage 1: plot)
  -ChapterS2Model CHAPTERS2MODEL
                        Model to use for writing the chapter (stage 2: character development)
  -ChapterS3Model CHAPTERS3MODEL
                        Model to use for writing the chapter (stage 3: dialogue)
  -ChapterS4Model CHAPTERS4MODEL
                        Model to use for writing the chapter (stage 4: final correction pass)
  -ChapterRevisionModel CHAPTERREVISIONMODEL
                        Model to use for revising the chapter until it meets criteria
  -RevisionModel REVISIONMODEL
                        Model to use for generating constructive criticism
  -EvalModel EVALMODEL  Model to use for evaluating the rating out of 100
  -InfoModel INFOMODEL  Model to use when generating summary/info at the end
  -ScrubModel SCRUBMODEL
                        Model to use when scrubbing the story at the end
  -CheckerModel CHECKERMODEL
                        Model to use when checking if the LLM cheated or not
  -TranslatorModel TRANSLATORMODEL
                        Model to use if translation of the story is enabled
  -Translate TRANSLATE  Specify a language to translate the story to - will not translate by default. Ex: 'French'
  -Seed SEED            Used to seed models.
  -OutlineMinRevisions OUTLINEMINREVISIONS
                        Number of minimum revisions that the outline must be given prior to proceeding
  -OutlineMaxRevisions OUTLINEMAXREVISIONS
                        Max number of revisions that the outline may have
  -ChapterMinRevisions CHAPTERMINREVISIONS
                        Number of minimum revisions that the chapter must be given prior to proceeding
  -ChapterMaxRevisions CHAPTERMAXREVISIONS
                        Max number of revisions that the chapter may have
  -NoChapterRevision    Disables Chapter Revisions
  -NoScrubChapters      Disables a final pass over the story to remove prompt leftovers/outline tidbits
  -ExpandOutline        Disables the system from expanding the outline for the story chapter by chapter prior to writing the story's chapter content
  -EnableFinalEditPass  Enable a final edit pass of the whole story prior to scrubbing
  -Debug                Print system prompts to stdout during generation

```

NOTE: due to the many LLMs used and the various edit/revision cycle loops, this project does not produce output quickly - on 3x TESLA P40 24GB GPUs, some stories take over 18 hours to generate. Faster hardware will of course result in lower generation time.



## Installation

Installing is pretty easy - just clone this repo, install [OLLAMA](https://ollama.com/) on some machine you have, and point the writer at it. 

For now, you also have to download the different LLMs that this project uses manually (sorry). Please see some of the test scripts for an idea of the models that I've been using so far.
The project uses a few different LLMs to generate different parts of the output (for example one for outline generation, another for each stage for the chapter generation, etc.), so make sure you have a few hundred GB of disk space free for this.

I've been developing on a machine with 3x NVIDIA TESLA P40 24GB GPUs, so all the models used by default (and in the testing scripts), are 70 billion parameters and up. I've not thoroughly experimented with smaller models as of yet - those likely aren't going to produce as good of a result, but they will definitely be much faster to run.


For now, Linux is the only thing supported - I don't use or like Windows or Mac, so I've not tested either platform. It might work, it might not - feel free to try though!
I run on a Debian distro, so that is what i'll write an installer script for, once the project matures enough to get there.


## Contributing

I welcome contributions, please either email me at `thomas.liao13 [at] gmail.com`, or open up a pull request (or both)!

If you encounter issues, please feel free to also open up an issue - I'll do my best to help with those!