#!/bin/bash
# Calculate seconds between Feb 24, 2022 and Jan 1, 2024
original_date="2022-02-24T15:58:49"
target_date="2024-01-01T00:00:00"

# Convert to seconds since epoch
original_seconds=$(date -d "$original_date" +%s 2>/dev/null || date -jf "%Y-%m-%dT%H:%M:%S" "$original_date" +%s)
target_seconds=$(date -d "$target_date" +%s 2>/dev/null || date -jf "%Y-%m-%dT%H:%M:%S" "$target_date" +%s)
offset=$((target_seconds - original_seconds))

export OFFSET=$offset

# Update the GIT_*_DATE variables
GIT_AUTHOR_DATE=$(date -d "@$(($(date -d "$(echo $GIT_AUTHOR_DATE | cut -d' ' -f1-2)" +%s) + $OFFSET))" +'%Y-%m-%d %H:%M:%S %z' 2>/dev/null) || \
GIT_AUTHOR_DATE=$(date -jf "%Y-%m-%d %H:%M:%S" -v+${OFFSET}S "$(echo $GIT_AUTHOR_DATE | cut -d' ' -f1-2)" +'%Y-%m-%d %H:%M:%S +0900')

export GIT_AUTHOR_DATE
export GIT_COMMITTER_DATE=$GIT_AUTHOR_DATE
