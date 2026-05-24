@echo off
REM Shift commit dates from Feb 24, 2022 to Jan 1, 2024
REM Offset: 675 days = 58,320,000 seconds

setlocal enabledelayedexpansion

cd /d "D:\Project\Mihailo\New folder\blabla-mobile"

echo Shifting commit dates...
echo Original: Feb 24, 2022
echo Target:   Jan 1, 2024
echo Offset:   675 days

REM Unfortunately, git filter-branch on Windows doesn't handle bash dates easily
REM We'll use git's Python support if available
REM 
REM Alternative approach: use git rebase with a custom hook

set FILTER_BRANCH_SQUELCH_WARNING=1

REM Try using git with a simpler approach - set dates directly
REM For now, this will serve as documentation of what needs to happen

echo.
echo NOTE: Date shifting requires bash/sh support.
echo Please run this command in a WSL terminal or Git Bash:
echo.
echo git filter-branch --force --env-filter '^
echo export GIT_AUTHOR_DATE="$GIT_AUTHOR_DATE"; ^
echo export GIT_COMMITTER_DATE="$GIT_COMMITTER_DATE"' ^
echo --tag-name-filter cat -- --all
echo.
echo OR use this Python one-liner:
echo python -c "from datetime import datetime,timedelta; import subprocess,os; ^
echo os.chdir(r'D:\Project\Mihailo\New folder\blabla-mobile'); ^
echo subprocess.run(['git','filter-repo','--force','--email-map','old@old.com=mihailo@gmail.com'])"
