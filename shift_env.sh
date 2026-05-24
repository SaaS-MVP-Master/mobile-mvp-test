#!/bin/bash
# Shift commit dates from Feb 24, 2022 to Feb 24, 2024 (730 days = 63,072,000 seconds)

if [ "$GIT_AUTHOR_DATE" != "" ]; then
  old_timestamp=$(date -d "$GIT_AUTHOR_DATE" +%s 2>/dev/null || date -jf "%Y-%m-%d %H:%M:%S %z" "$(echo "$GIT_AUTHOR_DATE" | sed 's/ [+-][0-9]*$//')" +%s 2>/dev/null)
  new_timestamp=$((old_timestamp + 63072000))
  new_date=$(date -d @$new_timestamp "+%Y-%m-%d %H:%M:%S %z" 2>/dev/null || date -r $new_timestamp "+%Y-%m-%d %H:%M:%S %z")
  export GIT_AUTHOR_DATE="$new_date"
  export GIT_COMMITTER_DATE="$new_date"
fi
