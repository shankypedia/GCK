#!/usr/bin/env python3
"""
Analytics for GitHub Contribution Keeper
Tracks and visualizes contribution patterns
"""

import os
import json
import datetime
import sqlite3
from pathlib import Path

# Database setup
DB_PATH = Path(__file__).parent.parent.parent / ".github" / "data" / "contribution_data.db"

def ensure_db_exists():
    """Ensure the database and tables exist"""
    # Create directory if it doesn't exist
    os.makedirs(DB_PATH.parent, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contributions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        commit_count INTEGER NOT NULL,
        project_type TEXT,
        season TEXT,
        collaboration TEXT,
        co_author TEXT,
        multiplier REAL,
        description TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contribution_id INTEGER,
        filepath TEXT NOT NULL,
        file_type TEXT,
        modification_type TEXT,
        FOREIGN KEY (contribution_id) REFERENCES contributions(id)
    )
    ''')
    
    conn.commit()
    conn.close()

def record_contribution(date, commit_count, project_type, files_modified, pattern=None):
    """Record a contribution to the database"""
    ensure_db_exists()
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Format date if it's a datetime object
    if isinstance(date, datetime.datetime):
        date = date.strftime("%Y-%m-%d")
    
    # Extract pattern data if provided
    season = None
    collaboration = None
    co_author = None
    multiplier = None
    description = None
    
    if pattern:
        season = pattern.get("season")
        collaboration = pattern.get("collaboration")
        co_author = pattern.get("co_author")
        multiplier = pattern.get("commit_multiplier")
        description = pattern.get("description")
    
    # Insert contribution record
    cursor.execute('''
    INSERT INTO contributions (date, commit_count, project_type, season, collaboration, co_author, multiplier, description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (date, commit_count, project_type, season, collaboration, co_author, multiplier, description))
    
    contribution_id = cursor.lastrowid
    
    # Insert file records
    for file_info in files_modified:
        filepath = file_info.get("filepath")
        file_type = file_info.get("file_type")
        modification_type = file_info.get("modification_type", "modify")
        
        cursor.execute('''
        INSERT INTO files (contribution_id, filepath, file_type, modification_type)
        VALUES (?, ?, ?, ?)
        ''', (contribution_id, filepath, file_type, modification_type))
    
    conn.commit()
    conn.close()

def get_contribution_stats(start_date=None, end_date=None):
    """Get statistics about contributions in a date range"""
    ensure_db_exists()
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    cursor = conn.cursor()
    
    # Build query based on date range
    query = "SELECT * FROM contributions"
    params = []
    
    if start_date or end_date:
        query += " WHERE"
        
        if start_date:
            query += " date >= ?"
            params.append(start_date if isinstance(start_date, str) else start_date.strftime("%Y-%m-%d"))
            
        if start_date and end_date:
            query += " AND"
            
        if end_date:
            query += " date <= ?"
            params.append(end_date if isinstance(end_date, str) else end_date.strftime("%Y-%m-%d"))
    
    # Execute query
    cursor.execute(query, params)
    contributions = [dict(row) for row in cursor.fetchall()]
    
    # Calculate statistics
    stats = {
        "total_contributions": len(contributions),
        "total_commits": sum(c["commit_count"] for c in contributions),
        "contribution_days": len(set(c["date"] for c in contributions)),
        "project_types": {},
        "seasons": {},
        "collaborations": {},
        "by_month": {},
        "by_day_of_week": {i: 0 for i in range(7)}  # 0=Monday, 6=Sunday
    }
    
    # Process each contribution
    for contrib in contributions:
        # Project types
        project_type = contrib["project_type"]
        if project_type:
            stats["project_types"][project_type] = stats["project_types"].get(project_type, 0) + 1
        
        # Seasons
        season = contrib["season"]
        if season:
            stats["seasons"][season] = stats["seasons"].get(season, 0) + 1
        
        # Collaborations
        collab = contrib["collaboration"]
        if collab:
            stats["collaborations"][collab] = stats["collaborations"].get(collab, 0) + 1
        
        # By month
        date = datetime.datetime.strptime(contrib["date"], "%Y-%m-%d")
        month_key = date.strftime("%Y-%m")
        stats["by_month"][month_key] = stats["by_month"].get(month_key, 0) + contrib["commit_count"]
        
        # By day of week
        day_of_week = date.weekday()  # 0=Monday, 6=Sunday
        stats["by_day_of_week"][day_of_week] += contrib["commit_count"]
    
    # Get file statistics
    cursor.execute('''
    SELECT f.file_type, COUNT(*) as count
    FROM files f
    JOIN contributions c ON f.contribution_id = c.id
    WHERE c.date BETWEEN ? AND ?
    GROUP BY f.file_type
    ''', [
        start_date if isinstance(start_date, str) else (start_date.strftime("%Y-%m-%d") if start_date else "2000-01-01"),
        end_date if isinstance(end_date, str) else (end_date.strftime("%Y-%m-%d") if end_date else "2100-01-01")
    ])
    
    stats["file_types"] = {row["file_type"]: row["count"] for row in cursor.fetchall()}
    
    conn.close()
    return stats

def generate_report(output_path=None, start_date=None, end_date=None):
    """Generate a JSON report of contribution statistics"""
    stats = get_contribution_stats(start_date, end_date)
    
    # Format dates for the report
    if start_date is None:
        # Get earliest date from database
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(date) FROM contributions")
        result = cursor.fetchone()
        start_date = result[0] if result and result[0] else datetime.datetime.now().strftime("%Y-%m-%d")
        conn.close()
    elif isinstance(start_date, datetime.datetime):
        start_date = start_date.strftime("%Y-%m-%d")
    
    if end_date is None:
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    elif isinstance(end_date, datetime.datetime):
        end_date = end_date.strftime("%Y-%m-%d")
    
    # Create report
    report = {
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date_range": {
            "start": start_date,
            "end": end_date
        },
        "statistics": stats
    }
    
    # Write to file if path provided
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
    
    return report

def get_streak_info():
    """Get information about contribution streaks"""
    ensure_db_exists()
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Get all contribution dates
    cursor.execute("SELECT date FROM contributions ORDER BY date")
    dates = [row[0] for row in cursor.fetchall()]
    
    if not dates:
        return {"current_streak": 0, "longest_streak": 0, "total_days": 0}
    
    # Convert to datetime objects
    date_objs = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    
    # Calculate streaks
    current_streak = 0
    longest_streak = 0
    streak_start = None
    
    # Check if today has a contribution
    today = datetime.datetime.now().date()
    yesterday = today - datetime.timedelta(days=1)
    
    if today in date_objs:
        current_streak = 1
        streak_start = today
    elif yesterday in date_objs:
        # Start checking from yesterday
        current_streak = 1
        streak_start = yesterday
    
    # Calculate longest streak
    for i in range(len(date_objs) - 1):
        # If consecutive days
        if (date_objs[i+1] - date_objs[i]).days == 1:
            if streak_start is None:
                streak_start = date_objs[i]
                current_streak = 2
            else:
                current_streak += 1
        else:
            # Streak broken
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1
            streak_start = date_objs[i+1]
    
    # Update longest streak with current streak
    longest_streak = max(longest_streak, current_streak)
    
    conn.close()
    
    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "total_days": len(set(date_objs))
    }

if __name__ == "__main__":
    # Test the analytics module
    ensure_db_exists()
    
    # Example: Record a test contribution
    today = datetime.datetime.now()
    record_contribution(
        date=today,
        commit_count=5,
        project_type="web-app",
        files_modified=[
            {"filepath": "src/index.js", "file_type": ".js", "modification_type": "modify"},
            {"filepath": "docs/README.md", "file_type": ".md", "modification_type": "create"}
        ],
        pattern={
            "season": "normal",
            "collaboration": None,
            "co_author": None,
            "commit_multiplier": 1.0,
            "description": "Normal season | Working on web-app"
        }
    )
    
    # Generate and print a report
    report = generate_report()
    print(json.dumps(report, indent=2))
    
    # Print streak information
    streak_info = get_streak_info()
    print(f"Current streak: {streak_info['current_streak']} days")
    print(f"Longest streak: {streak_info['longest_streak']} days")
    print(f"Total contribution days: {streak_info['total_days']}")
