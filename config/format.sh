#!/bin/sh

# Provide filenames as arguments to only format some files.
FILES="$*"

# Otherwise, format all of them.
if [ -z "$FILES" ] ; then
    TOP_LEVEL_FILES=`find . -type f -name \*.py -maxdepth 1`
    COMMUNITYSHARE_FILES=`find community_share -type f -name \*.py`
    FILES="$TOP_LEVEL_FILES $COMMUNITYSHARE_FILES"
fi

yapf -i $FILES
