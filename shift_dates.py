#!/usr/bin/env python3
import subprocess
import os
import sys
from datetime import datetime, timedelta

os.chdir(r"D:\Project\Mihailo\New folder\blabla-mobile")

# Calculate offset between Feb 24, 2022 and Jan 1, 2024
original_earliest = datetime(2022, 2, 24)
target_date = datetime(2024, 1, 1)
offset_days = (target_date - original_earliest).days
offset_seconds = int((target_date - original_earliest).total_seconds())

print(f"Shifting commits by {offset_days} days ({offset_seconds} seconds)")

# Create the filter-branch command
cmd = [
    'git', 'filter-branch', '--force',
    '--env-filter',
    f'''
import os
from datetime import datetime, timedelta

offset_seconds = {offset_seconds}

# Parse current dates
author_date_str = os.environ.get('GIT_AUTHOR_DATE', '')
committer_date_str = os.environ.get('GIT_COMMITTER_DATE', '')

if author_date_str:
    # Parse the date format "2022-02-24 15:58:49 +0900"
    parts = author_date_str.split()
    date_part = parts[0]  # YYYY-MM-DD
    time_part = parts[1]  # HH:MM:SS
    tz_part = parts[2]    # +0900
    
    dt = datetime.strptime(date_part + ' ' + time_part, '%Y-%m-%d %H:%M:%S')
    new_dt = dt + timedelta(seconds={offset_seconds})
    new_date_str = new_dt.strftime('%Y-%m-%d %H:%M:%S') + ' ' + tz_part
    
    os.environ['GIT_AUTHOR_DATE'] = new_date_str
    os.environ['GIT_COMMITTER_DATE'] = new_date_str
''',
    '--tag-name-filter', 'cat',
    '--', '--all'
]

env = os.environ.copy()
env['FILTER_BRANCH_SQUELCH_WARNING'] = '1'

result = subprocess.run(cmd, env=env)
sys.exit(result.returncode)
