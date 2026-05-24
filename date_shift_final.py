#!/usr/bin/env python3
"""
Shift git commit dates from Feb 24, 2022 to Feb 24, 2024 (730 days forward)
while preserving relative time spacing between commits.
"""
import subprocess
import os
import sys
from datetime import datetime, timedelta

os.chdir(r"D:\Project\Mihailo\New folder\blabla-mobile")

# Get all commits in reverse order (oldest first)
result = subprocess.run(
    ["git", "log", "--reverse", "--all", "--format=%H|%aI"],
    capture_output=True,
    text=True,
    check=True
)

commits = []
for line in result.stdout.strip().split('\n'):
    if line and '|' in line:
        commit_hash, date_str = line.split('|', 1)
        commits.append((commit_hash, date_str))

if not commits:
    print("No commits found")
    sys.exit(1)

# Parse first and last commit dates
first_commit_date = datetime.fromisoformat(commits[0][1])
last_commit_date = datetime.fromisoformat(commits[-1][1])

# Target range: Feb 24, 2024 to Jan 1, 2024 (preserve the span)
target_first_date = datetime(2024, 2, 24, tzinfo=first_commit_date.tzinfo)

# Calculate offset
offset = target_first_date - first_commit_date
offset_seconds = int(offset.total_seconds())

print(f"Found {len(commits)} commits")
print(f"Original date range: {first_commit_date} to {last_commit_date}")
print(f"Target first date: {target_first_date}")
print(f"Offset: {offset_seconds} seconds ({offset.days} days)")
print()

# Build the environment filter script as a string
env_filter = f'''
import os
import sys
from datetime import datetime, timedelta

offset_seconds = {offset_seconds}

author_date = os.environ.get('GIT_AUTHOR_DATE', '')
if author_date:
    try:
        dt = datetime.fromisoformat(author_date)
        new_dt = dt + timedelta(seconds=offset_seconds)
        new_date_str = new_dt.isoformat()
        os.environ['GIT_AUTHOR_DATE'] = new_date_str
        os.environ['GIT_COMMITTER_DATE'] = new_date_str
        # Update them in place for export
        sys.stderr.write(f"export GIT_AUTHOR_DATE='{{new_date_str}}'\\n")
        sys.stderr.write(f"export GIT_COMMITTER_DATE='{{new_date_str}}'\\n")
    except Exception as e:
        sys.stderr.write(f"Error: {{e}}\\n")
        sys.exit(1)
'''

# Set environment and run filter-branch
env = os.environ.copy()
env['FILTER_BRANCH_SQUELCH_WARNING'] = '1'

print("Running git filter-branch to shift commit dates...")
print("This may take a minute...")
print()

# Use git filter-branch with the environment variables directly
# Since we can't easily use Python as the env-filter from PowerShell,
# we'll use a simpler approach: modify AUTHORS and use that

# Alternative: Create a mapping file
import tempfile
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, dir='.') as f:
    filter_file = f.name
    # This won't work either on Windows...

# Best approach for Windows: Use git-filter-repo if available
check_filter_repo = subprocess.run(
    ["git", "filter-repo", "--help"],
    capture_output=True,
    text=True
)

if check_filter_repo.returncode == 0:
    print("Using git-filter-repo (recommended tool)...")
    # Create a commit map file
    with open('commit-map.txt', 'w') as f:
        # Format: old-hash new-hash
        for old_hash, date_str in commits:
            dt = datetime.fromisoformat(date_str)
            new_dt = dt + timedelta(seconds=offset_seconds)
            f.write(f"{old_hash}=mihailo <mihailoracke004@gmail.com> {int(new_dt.timestamp())} +0900\n")
    
    print("Filter-repo available, proceeding...")
else:
    print("git-filter-repo not available. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "git-filter-repo"], check=True)

# Execute the date shift using filter-branch with inline Python script
# On Windows, this is tricky. We'll document what needs to happen.
print("\nNote: Full date rewriting requires bash/Unix shell environment.")
print("Recommended approaches:")
print("1. Use Git Bash: Right-click → Git Bash Here")
print("2. Use WSL: wsl bash")
print("3. Install git-filter-repo: pip install git-filter-repo")
print()
print("Command to run in Git Bash:")
print(f'git filter-branch --force --env-filter \'export GIT_AUTHOR_DATE="$(date -d @$((\\$(date -d "${{GIT_AUTHOR_DATE}}" +%s) + {offset_seconds})) \'+%Y-%m-%d %H:%M:%S %z\')\"; export GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE"\' --tag-name-filter cat -- --all')
