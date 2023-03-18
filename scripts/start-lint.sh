#!/bin/sh

# Project Folders
TARGET_FOLDERS="source"
MAX_ACCEPTABLE_COMPLEXITY=6

# Run Tools
echo "Running isort" && \
    isort $TARGET_FOLDERS -c --diff && \
    echo "Running black..." && \
    black --check --diff $TARGET_FOLDERS && \
    echo "Running pycodestyle..."&& \
    pycodestyle $TARGET_FOLDERS && \
    echo "Performing general code quality evaluation ..."&& \
    flake8 $TARGET_FOLDERS && \
    echo "Running some static typing checking..." && \
    mypy $TARGET_FOLDERS &&
    echo "Checking for cyclomatic complexity" && \
    flake8 --max-complexity $MAX_ACCEPTABLE_COMPLEXITY $TARGET_FOLDERS

