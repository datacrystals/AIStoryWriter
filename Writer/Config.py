WRITER_MODEL="vanilj/midnight-miqu-70b-v1.5" # Note this value is overridden by the argparser
REVISION_MODEL="llama3:70b" # Note this value is overridden by the argparser
EVAL_MODEL="llama3:70b" # Note this value is overridden by the argparser
INFO_MODEL="llama3:70b" # Note this value is overridden by the argparser

SEED=12 # Note this value is overridden by the argparser

OUTLINE_QUALITY=87 # Note this value is overridden by the argparser
OUTLINE_MIN_REVISIONS=0 # Note this value is overridden by the argparser
OUTLINE_MAX_REVISIONS=3 # Note this value is overridden by the argparser
CHAPTER_NO_REVISIONS=True # Note this value is overridden by the argparser # disables all revision checks for the chapter, overriding any other chapter quality/revision settings
CHAPTER_QUALITY=85 # Note this value is overridden by the argparser
CHAPTER_MIN_REVISIONS=1 # Note this value is overridden by the argparser
CHAPTER_MAX_REVISIONS=3 # Note this value is overridden by the argparser

# We also have
"llama3"
"llama3:70b"
"vanilj/midnight-miqu-70b-v1.5"
"mixtral:8x22b"
"nous-hermes2"
"command-r"
"qwen:72b"
"command-r-plus"
"dbrx"