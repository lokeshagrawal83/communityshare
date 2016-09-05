#!/bin/sh

# Provide file/directory names as arguments to only lint some files.
FILES="$*"

# Otherwise, lint all of them.
if [ -z "$FILES" ] ; then
    DIRS="./static/js/controllers ./static/js/directives ./static/js/services"
    TOP_LEVEL_FILES="./static/js/index.js ./static/js/main.js"

    FILES="$DIRS $TOP_LEVEL_FILES"
fi

./node_modules/.bin/eslint $FILES
