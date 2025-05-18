#!/usr/bin/env python3
"""
GitHub Contribution Keeper
Creates realistic commit patterns to maintain an active GitHub contribution graph
"""

import os
import random
import datetime
import time
import subprocess
import sys
from pathlib import Path

# Import our custom modules
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

try:
    from commit_messages import get_random_commit_message
    from file_generator import create_or_modify_random_file
    from user_config import (
        get_user_name, get_random_user_email, 
        get_commit_time_probability, get_commit_count_for_day,
        is_vacation_day, get_random_project_type
    )
except ImportError:
    print("Error: Required modules not found. Make sure all required modules exist.")
    sys.exit(1)

def configure_git():
    """Configure git with user information"""
    name = get_user_name()
    email = get_random_user_email()
    
    subprocess.run(['git', 'config', 'user.name', name], check=True)
    subprocess.run(['git', 'config', 'user.email', email], check=True)
    
    print(f"Git configured with: {name} <{email}>")

def create_commit(project_type=None):
    """Create a single commit with realistic changes and message"""
    # Create or modify a random file
    modified_file = create_or_modify_random_file(project_type)
    
    # Generate a commit message
    commit_message = get_random_commit_message(project_type)
    
    # Add the file to git
    subprocess.run(['git', 'add', modified_file], check=True)
    
    # Create the commit
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)
    
    print(f"Created commit: '{commit_message}' (modified {modified_file})")

def add_commits(force_count=None):
    """Add a realistic number of commits based on day patterns"""
    today = datetime.datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    
    # Check if today is a vacation day
    if is_vacation_day(today_str) and not force_count:
        print(f"Today ({today_str}) is a vacation day. No commits.")
        return
    
    # Determine commit count
    if force_count:
        commit_count = int(force_count)
    else:
        day_of_week = today.weekday()
        commit_count = get_commit_count_for_day(day_of_week)
    
    print(f"Will create {commit_count} commits today ({today_str})")
    
    # Select a project type for today's commits
    project_type = get_random_project_type()
    print(f"Today's project focus: {project_type['name']}")
    
    # Create commits with realistic timing
    for i in range(commit_count):
        create_commit(project_type)
        
        # Add a realistic delay between commits
        if i < commit_count - 1:
            # Shorter delays for consecutive commits
            delay = random.uniform(30, 300)  # 30 seconds to 5 minutes
            print(f"Waiting {delay:.1f} seconds before next commit...")
            time.sleep(delay)

if __name__ == "__main__":
    # Check for environment variables
    force_count = os.environ.get('COMMIT_COUNT')
    force_run = os.environ.get('FORCE_RUN', 'false').lower() == 'true'
    
    # Ensure we're in the repository root
    repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode().strip()
    os.chdir(repo_root)
    
    # Configure git with user information
    configure_git()
    
    print(f"Starting contribution process at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run the contribution process
    add_commits(force_count if force_run or force_count else None)
    
    print(f"Finished at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
