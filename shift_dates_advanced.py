#!/usr/bin/env python3
"""
Shift git commit dates from 2022 to 2024 while preserving relative spacing.
"""
import subprocess
import os
import sys
from datetime import datetime, timedelta

os.chdir(r"D:\Project\Mihailo\New folder\blabla-mobile")

# Get all commits
result = subprocess.run(
    ["git", "log", "--reverse", "--all", "--format=%H %aI"],
    capture_output=True,
    text=True,
    check=True
)

commits = []
for line in result.stdout.strip().split('\n'):
    if line:
        parts = line.split()
        commit_hash = parts[0]
        date_str = ' '.join(parts[1:])
        commits.append((commit_hash, date_str))

if not commits:
    print("No commits found")
    sys.exit(1)

# Parse first commit date
first_commit_date_str = commits[0][1]
first_commit_date = datetime.fromisoformat(first_commit_date_str)

# Target date: Jan 1, 2024
target_date = datetime(2024, 1, 1, tzinfo=first_commit_date.tzinfo)

# Calculate offset
offset = target_date - first_commit_date
offset_seconds = int(offset.total_seconds())

print(f"Original first commit: {first_commit_date}")
print(f"Target date: {target_date}")
print(f"Offset: {offset_seconds} seconds ({offset.days} days)")

# Use git filter-branch with a Python script for date shifting
filter_script = f'''
import os
from datetime import datetime, timedelta
import sys

offset_seconds = {offset_seconds}

# Get the current dates
author_date = os.environ.get('GIT_AUTHOR_DATE', '')
committer_date = os.environ.get('GIT_COMMITTER_DATE', '')

if author_date:
    try:
        dt = datetime.fromisoformat(author_date)
        new_dt = dt + timedelta(seconds=offset_seconds)
        new_date_str = new_dt.isoformat()
        os.environ['GIT_AUTHOR_DATE'] = new_date_str
        os.environ['GIT_COMMITTER_DATE'] = new_date_str
    except Exception as e:
        print(f"Error parsing date: {{e}}", file=sys.stderr)
        sys.exit(1)

# Export the updated environment variables
for key in ['GIT_AUTHOR_DATE', 'GIT_COMMITTER_DATE']:
    val = os.environ.get(key)
    if val:
        print(f"export {{key}}={{repr(val)}}", file=sys.stderr)
'''

env = os.environ.copy()
env['FILTER_BRANCH_SQUELCH_WARNING'] = '1'

# Note: This approach requires a custom shell integration which is complex on Windows
# Instead, we'll use git directly with rebase
print("\nNote: Using git rebase approach for date shifting...")

# Alternative: Use git rebase with custom filter
subprocess.run(
    ["git", "rebase", "--force-rebase", "--root", "--exec", "GIT_AUTHOR_DATE=$(date -d '+675 days' -f) GIT_COMMITTER_DATE=$(date -d '+675 days' -f) git commit --amend --no-edit -C HEAD"],
    env=env,
    check=False
)
