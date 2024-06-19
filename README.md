# AI Story Generatior

This project aims to be a LLM-based story generator which produces medium to full-length novels based on a user-provided prompt.

So far, it's a work in progress, as I'm still focusing on getting the bugs worked out and improving the generated output quality.


## Usage

This system will generate a story based on a user provided prompt. Simply create a file with your intended prompt in a text file, and pass the path to that as a parameter (use ./Write.py --help) to get a full list of parameters.

As of 2024-06-19, here's an example usage command, but make sure to check for any updated test scripts as those will be more up-to-date than this readme.

Make sure to substitute in values for your OLLAMA host and prompt path.

```sh

./Write.py \
-Host [OLLAMA HOST HERE]:11434 \
-Seed 999 \
-Prompt Path/To/Your/Prompt/File/Here \
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
-Debug \
-NoChapterRevision

```

Here's a full list of arguments as of 2024-06-19:

```
usage: Write.py [-h] [-Prompt PROMPT] [-Output OUTPUT] [-Host HOST] [-InitialOutlineModel INITIALOUTLINEMODEL] [-ChapterOutlineModel CHAPTEROUTLINEMODEL] [-ChapterS1Model CHAPTERS1MODEL] [-ChapterS2Model CHAPTERS2MODEL]
                [-ChapterS3Model CHAPTERS3MODEL] [-ChapterS4Model CHAPTERS4MODEL] [-ChapterRevisionModel CHAPTERREVISIONMODEL] [-RevisionModel REVISIONMODEL] [-EvalModel EVALMODEL] [-InfoModel INFOMODEL] [-ScrubModel SCRUBMODEL]
                [-CheckerModel CHECKERMODEL] [-Seed SEED] [-OutlineMinRevisions OUTLINEMINREVISIONS] [-OutlineMaxRevisions OUTLINEMAXREVISIONS] [-ChapterMinRevisions CHAPTERMINREVISIONS]
                [-ChapterMaxRevisions CHAPTERMAXREVISIONS] [-NoChapterRevision] [-NoScrubChapters] [-ExpandOutline] [-EnableFinalEditPass] [-Debug]

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



## Installation

Installing is pretty easy - just clone this repo, install [OLLAMA](https://ollama.com/) on some machine you have, and point the writer at it. 

For now, you also have to download the different LLMs that this project uses manually (sorry). Please see some of the test scripts for an idea of the models that I've been using so far.
The project uses a few different LLMs to generate different parts of the output (for example one for outline generation, another for each stage for the chapter generation, etc.), so make sure you have a few hundred GB of disk space free for this.

I've been developing on a machine with 3x NVIDIA TESLA P40 24GB GPUs, so all the models used by default (and in the testing scripts), are 70 billion parameters and up. I've not thoroughly experimented with smaller models as of yet - those likely aren't going to produce as good of a result, but they will definitely be much faster to run.


For now, Linux is the only thing supported - I don't use or like Windows or Mac, so I've not tested either platform. It might work, it might not - feel free to try though!
I run on a Debian distro, so that is what i'll write an installer script for, once the project matures enough to get there.
