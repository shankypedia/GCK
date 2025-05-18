#!/usr/bin/env python3
"""
Historical backfill for GitHub Contribution Keeper
Creates commits with past dates to fill in contribution history
"""

import os
import random
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Import our custom modules
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

try:
    from commit_messages import get_random_commit_message
    from file_generator import create_or_modify_random_file
    from user_config import get_user_name, get_random_user_email, get_commit_count_for_day, is_vacation_day
except ImportError:
    print("Error: Required modules not found.")
    sys.exit(1)

def get_start_date():
    """Return the start date for historical backfill (July 2020)"""
    return datetime(2020, 7, 1)

def get_end_date():
    """Return the end date for historical backfill (yesterday)"""
    return datetime.now() - timedelta(days=1)

def create_historical_commit(date):
    """Create a commit with a specific historical date"""
    # Format date for Git
    date_str = date.strftime("%Y-%m-%d %H:%M:%S")
    
    # Create or modify a random file
    modified_file = create_or_modify_random_file()
    
    # Generate a commit message
    commit_message = get_random_commit_message()
    
    # Add the file to git
    subprocess.run(['git', 'add', modified_file], check=True)
    
    # Set the author and committer information
    name = get_user_name()
    email = get_random_user_email()
    
    # Create the commit with the historical date
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    subprocess.run([
        'git', 'commit', 
        '-m', commit_message,
        '--author', f"{name} <{email}>"
    ], env=env, check=True)
    
    print(f"Created historical commit for {date_str}: '{commit_message}' (modified {modified_file})")

def backfill_history(start_date=None, end_date=None, max_days=None):
    """Create commits with dates in the past to fill contribution history"""
    if start_date is None:
        start_date = get_start_date()
    
    if end_date is None:
        end_date = get_end_date()
    
    # Limit the number of days to process if specified
    if max_days is not None:
        days_diff = (end_date - start_date).days
        if days_diff > max_days:
            start_date = end_date - timedelta(days=max_days)
    
    print(f"Backfilling history from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Process each day in the range
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Skip vacation days
        if is_vacation_day(date_str):
            print(f"Skipping vacation day: {date_str}")
            current_date += timedelta(days=1)
            continue
        
        # Get commit count for this day of week
        day_of_week = current_date.weekday()  # 0 = Monday, 6 = Sunday
        commit_count = get_commit_count_for_day(day_of_week)
        
        if commit_count > 0:
            print(f"Creating {commit_count} commits for {date_str}")
            
            for i in range(commit_count):
                # Create a random time for the commit
                hour = random.randint(9, 22)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                
                commit_date = current_date.replace(hour=hour, minute=minute, second=second)
                create_historical_commit(commit_date)
        else:
            print(f"No commits scheduled for {date_str}")
        
        # Move to next day
        current_date += timedelta(days=1)

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    
    parser = argparse.ArgumentParser(description="Backfill GitHub contribution history")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--max-days", type=int, help="Maximum number of days to process")
    args = parser.parse_args()
    
    # Convert date strings to datetime objects if provided
    start_date = datetime.strptime(args.start, "%Y-%m-%d") if args.start else None
    end_date = datetime.strptime(args.end, "%Y-%m-%d") if args.end else None
    
    # Ensure we're in the repository root
    repo_root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode().strip()
    os.chdir(repo_root)
    
    # Run the backfill
    backfill_history(start_date, end_date, args.max_days)
    
    print("Historical backfill completed")
