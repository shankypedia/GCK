#!/usr/bin/env python3
"""
Smart Learning for GitHub Contribution Keeper
Adapts to your actual contribution patterns
"""

import os
import json
import datetime
import sqlite3
import subprocess
import statistics
import random
from pathlib import Path

# Database setup
DB_PATH = Path(__file__).parent.parent / "data" / "learning_data.db"

def ensure_db_exists():
    """Ensure the database and tables exist"""
    # Create directory if it doesn't exist
    os.makedirs(DB_PATH.parent, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS actual_contributions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        commit_count INTEGER NOT NULL,
        day_of_week INTEGER NOT NULL,
        is_weekend INTEGER NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS time_patterns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hour INTEGER NOT NULL,
        commit_count INTEGER NOT NULL,
        day_of_week INTEGER NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS learned_patterns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pattern_type TEXT NOT NULL,
        pattern_key TEXT NOT NULL,
        pattern_value REAL NOT NULL,
        updated_at TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

def fetch_actual_contributions(days=90):
    """Fetch actual GitHub contributions from the last N days"""
    try:
        # Get the repository directory
        repo_dir = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode().strip()
        
        # Calculate date range
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        # Format dates for git log
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # Get commit counts by date
        git_log = subprocess.check_output([
            'git', 'log', 
            f'--since={start_date_str}', 
            f'--until={end_date_str}', 
            '--format=%ad', '--date=short'
        ], cwd=repo_dir).decode()
        
        # Count commits by date
        commit_dates = git_log.strip().split('\n')
        commit_counts = {}
        
        for date in commit_dates:
            if date:  # Skip empty lines
                commit_counts[date] = commit_counts.get(date, 0) + 1
        
        # Convert to list of records
        contributions = []
        
        for date_str, count in commit_counts.items():
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            day_of_week = date_obj.weekday()  # 0=Monday, 6=Sunday
            is_weekend = 1 if day_of_week >= 5 else 0
            
            contributions.append({
                "date": date_str,
                "commit_count": count,
                "day_of_week": day_of_week,
                "is_weekend": is_weekend
            })
        
        return contributions
    
    except Exception as e:
        print(f"Error fetching actual contributions: {e}")
        return []

def fetch_commit_times(days=30):
    """Fetch actual commit times from the last N days"""
    try:
        # Get the repository directory
        repo_dir = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode().strip()
        
        # Calculate date range
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=days)
        
        # Format dates for git log
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # Get commit times
        git_log = subprocess.check_output([
            'git', 'log', 
            f'--since={start_date_str}', 
            f'--until={end_date_str}', 
            '--format=%ad', '--date=iso'
        ], cwd=repo_dir).decode()
        
        # Parse commit times
        commit_times = []
        
        for line in git_log.strip().split('\n'):
            if line:  # Skip empty lines
                try:
                    # Parse ISO format datetime
                    dt = datetime.datetime.fromisoformat(line.replace('Z', '+00:00'))
                    # Convert to local time
                    local_dt = dt.astimezone(datetime.datetime.now().astimezone().tzinfo)
                    
                    hour = local_dt.hour
                    day_of_week = local_dt.weekday()
                    
                    commit_times.append({
                        "hour": hour,
                        "day_of_week": day_of_week
                    })
                except Exception as e:
                    print(f"Error parsing date: {line} - {e}")
        
        return commit_times
    
    except Exception as e:
        print(f"Error fetching commit times: {e}")
        return []

def store_actual_patterns():
    """Fetch and store actual contribution patterns"""
    ensure_db_exists()
    
    # Fetch actual contributions
    contributions = fetch_actual_contributions()
    commit_times = fetch_commit_times()
    
    if not contributions and not commit_times:
        print("No actual contributions found to learn from")
        return False
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Store contribution data
    for contrib in contributions:
        cursor.execute('''
        INSERT INTO actual_contributions (date, commit_count, day_of_week, is_weekend)
        VALUES (?, ?, ?, ?)
        ''', (
            contrib["date"],
            contrib["commit_count"],
            contrib["day_of_week"],
            contrib["is_weekend"]
        ))
    
    # Store time pattern data
    for time_data in commit_times:
        cursor.execute('''
        INSERT INTO time_patterns (hour, commit_count, day_of_week)
        VALUES (?, ?, ?)
        ''', (
            time_data["hour"],
            1,  # Each entry represents one commit
            time_data["day_of_week"]
        ))
    
    conn.commit()
    conn.close()
    
    # Learn patterns from the stored data
    learn_patterns()
    
    return True

def learn_patterns():
    """Learn patterns from stored actual contributions"""
    ensure_db_exists()
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    patterns = {}
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Learn day of week patterns
    cursor.execute('''
    SELECT day_of_week, AVG(commit_count) as avg_commits
    FROM actual_contributions
    GROUP BY day_of_week
    ''')
    
    day_patterns = cursor.fetchall()
    for day, avg_commits in day_patterns:
        pattern_key = f"day_{day}"
        patterns[f"day_of_week:{pattern_key}"] = avg_commits
    
    # Learn weekend vs weekday patterns
    cursor.execute('''
    SELECT is_weekend, AVG(commit_count) as avg_commits
    FROM actual_contributions
    GROUP BY is_weekend
    ''')
    
    weekend_patterns = cursor.fetchall()
    for is_weekend, avg_commits in weekend_patterns:
        pattern_key = "weekend" if is_weekend else "weekday"
        patterns[f"weekend:{pattern_key}"] = avg_commits
    
    # Learn hour of day patterns
    cursor.execute('''
    SELECT hour, COUNT(*) as commit_count
    FROM time_patterns
    GROUP BY hour
    ''')
    
    hour_patterns = cursor.fetchall()
    total_hour_commits = sum(count for _, count in hour_patterns)
    
    for hour, count in hour_patterns:
        # Convert to probability
        probability = count / total_hour_commits if total_hour_commits > 0 else 0
        pattern_key = f"hour_{hour}"
        patterns[f"hour_of_day:{pattern_key}"] = probability
    
    # Store learned patterns
    for pattern_type_key, value in patterns.items():
        pattern_type, pattern_key = pattern_type_key.split(':')
        
        # Check if pattern already exists
        cursor.execute('''
        SELECT id FROM learned_patterns
        WHERE pattern_type = ? AND pattern_key = ?
        ''', (pattern_type, pattern_key))
        
        result = cursor.fetchone()
        
        if result:
            # Update existing pattern
            cursor.execute('''
            UPDATE learned_patterns
            SET pattern_value = ?, updated_at = ?
            WHERE pattern_type = ? AND pattern_key = ?
            ''', (value, now, pattern_type, pattern_key))
        else:
            # Insert new pattern
            cursor.execute('''
            INSERT INTO learned_patterns (pattern_type, pattern_key, pattern_value, updated_at)
            VALUES (?, ?, ?, ?)
            ''', (pattern_type, pattern_key, value, now))
    
    conn.commit()
    conn.close()
    
    return patterns

def get_learned_patterns():
    """Get all learned patterns"""
    ensure_db_exists()
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM learned_patterns')
    
    patterns = {}
    for row in cursor.fetchall():
        pattern_type = row['pattern_type']
        pattern_key = row['pattern_key']
        pattern_value = row['pattern_value']
        
        if pattern_type not in patterns:
            patterns[pattern_type] = {}
        
        patterns[pattern_type][pattern_key] = pattern_value
    
    conn.close()
    return patterns

def get_commit_count_for_day(day_of_week, is_weekend=None):
    """Get learned commit count for a specific day"""
    patterns = get_learned_patterns()
    
    # If we have day-specific patterns, use those
    if 'day_of_week' in patterns and f'day_{day_of_week}' in patterns['day_of_week']:
        return patterns['day_of_week'][f'day_{day_of_week}']
    
    # Fall back to weekend/weekday pattern
    if is_weekend is None:
        is_weekend = day_of_week >= 5  # 5=Saturday, 6=Sunday
    
    if 'weekend' in patterns:
        pattern_key = 'weekend' if is_weekend else 'weekday'
        if pattern_key in patterns['weekend']:
            return patterns['weekend'][pattern_key]
    
    # Fall back to default values if no learned patterns
    if is_weekend:
        return random.randint(0, 3)  # Fewer commits on weekends
    else:
        return random.randint(1, 8)  # More commits on weekdays

def get_commit_hour_probability(hour):
    """Get probability of committing at a specific hour"""
    patterns = get_learned_patterns()
    
    if 'hour_of_day' in patterns and f'hour_{hour}' in patterns['hour_of_day']:
        return patterns['hour_of_day'][f'hour_{hour}']
    
    # Fall back to default values if no learned patterns
    if 9 <= hour <= 17:  # 9 AM to 5 PM
        return 0.8
    elif 7 <= hour <= 8 or 18 <= hour <= 21:  # Early morning or evening
        return 0.4
    else:  # Late night
        return 0.1

def generate_adaptive_schedule(days=30):
    """Generate a commit schedule based on learned patterns"""
    patterns = get_learned_patterns()
    
    if not patterns:
        print("No learned patterns available. Using default patterns.")
        store_actual_patterns()  # Try to learn patterns
        patterns = get_learned_patterns()
    
    schedule = []
    start_date = datetime.datetime.now()
    
    for i in range(days):
        date = start_date + datetime.timedelta(days=i)
        day_of_week = date.weekday()
        is_weekend = day_of_week >= 5
        
        # Get commit count for this day
        commit_count = round(get_commit_count_for_day(day_of_week, is_weekend))
        
        # Skip days with no commits
        if commit_count <= 0:
            continue
        
        # Generate commit times based on hour probabilities
        commit_times = []
        hour_probs = []
        
        # Get hour probabilities
        for hour in range(24):
            prob = get_commit_hour_probability(hour)
            hour_probs.append((hour, prob))
        
        # Normalize probabilities
        total_prob = sum(prob for _, prob in hour_probs)
        if total_prob > 0:
            normalized_probs = [(hour, prob/total_prob) for hour, prob in hour_probs]
        else:
            # Fallback to uniform distribution
            normalized_probs = [(hour, 1/24) for hour in range(24)]
        
        # Select hours based on probabilities
        hours = [h for h, _ in normalized_probs]
        probs = [p for _, p in normalized_probs]
        
        selected_hours = random.choices(hours, weights=probs, k=commit_count)
        
        # Add minutes and seconds
        for hour in selected_hours:
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_time = date.replace(hour=hour, minute=minute, second=second)
            commit_times.append(commit_time)
        
        # Sort commit times
        commit_times.sort()
        
        schedule.append({
            "date": date.strftime("%Y-%m-%d"),
            "commit_count": commit_count,
            "commit_times": [t.strftime("%Y-%m-%d %H:%M:%S") for t in commit_times]
        })
    
    return schedule

def analyze_contribution_trends():
    """Analyze trends in contribution patterns"""
    ensure_db_exists()
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Get all contribution data
    cursor.execute('''
    SELECT date, commit_count, day_of_week, is_weekend
    FROM actual_contributions
    ORDER BY date
    ''')
    
    contributions = cursor.fetchall()
    
    if not contributions:
        conn.close()
        return {
            "status": "insufficient_data",
            "message": "Not enough contribution data for trend analysis"
        }
    
    # Convert to list of dictionaries
    contrib_data = []
    for date_str, count, day_of_week, is_weekend in contributions:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        contrib_data.append({
            "date": date_obj,
            "count": count,
            "day_of_week": day_of_week,
            "is_weekend": is_weekend
        })
    
    # Sort by date
    contrib_data.sort(key=lambda x: x["date"])
    
    # Calculate trends
    trends = {
        "total_contributions": sum(c["count"] for c in contrib_data),
        "total_days": len(contrib_data),
        "average_per_day": sum(c["count"] for c in contrib_data) / len(contrib_data),
        "weekday_avg": 0,
        "weekend_avg": 0,
        "day_of_week_avg": {i: 0 for i in range(7)},  # 0=Monday, 6=Sunday
        "monthly_trend": {},
        "trend_direction": "stable"
    }
    
    # Calculate weekday vs weekend averages
    weekday_counts = [c["count"] for c in contrib_data if c["is_weekend"] == 0]
    weekend_counts = [c["count"] for c in contrib_data if c["is_weekend"] == 1]
    
    if weekday_counts:
        trends["weekday_avg"] = sum(weekday_counts) / len(weekday_counts)
    
    if weekend_counts:
        trends["weekend_avg"] = sum(weekend_counts) / len(weekend_counts)
    
    # Calculate day of week averages
    for day in range(7):
        day_counts = [c["count"] for c in contrib_data if c["day_of_week"] == day]
        if day_counts:
            trends["day_of_week_avg"][day] = sum(day_counts) / len(day_counts)
    
    # Calculate monthly trends
    months = {}
    for contrib in contrib_data:
        month_key = contrib["date"].strftime("%Y-%m")
        if month_key not in months:
            months[month_key] = []
        months[month_key].append(contrib["count"])
    
    for month, counts in months.items():
        trends["monthly_trend"][month] = sum(counts) / len(counts)
    
    # Determine trend direction
    if len(months) >= 2:
        month_keys = sorted(months.keys())
        first_month = month_keys[0]
        last_month = month_keys[-1]
        
        first_avg = trends["monthly_trend"][first_month]
        last_avg = trends["monthly_trend"][last_month]
        
        if last_avg > first_avg * 1.2:
            trends["trend_direction"] = "increasing"
        elif last_avg < first_avg * 0.8:
            trends["trend_direction"] = "decreasing"
        else:
            trends["trend_direction"] = "stable"
    
    conn.close()
    return trends

def get_contribution_recommendations():
    """Generate recommendations based on learned patterns"""
    trends = analyze_contribution_trends()
    
    recommendations = []
    
    # Check if we have enough data
    if trends.get("status") == "insufficient_data":
        recommendations.append({
            "type": "data_collection",
            "message": "Continue contributing to build up pattern data",
            "priority": "high"
        })
        return recommendations
    
    # Check overall trend
    if trends["trend_direction"] == "decreasing":
        recommendations.append({
            "type": "activity_level",
            "message": "Your contribution level is decreasing. Consider increasing activity to maintain momentum.",
            "priority": "high"
        })
    
    # Check weekday vs weekend balance
    weekday_ratio = trends["weekday_avg"] / (trends["weekend_avg"] + 0.1)  # Avoid division by zero
    
    if weekday_ratio > 10:
        recommendations.append({
            "type": "work_balance",
            "message": "Your contributions are heavily weighted toward weekdays. Consider occasional weekend activity for more natural patterns.",
            "priority": "medium"
        })
    
    # Check day of week distribution
    day_avgs = trends["day_of_week_avg"]
    max_day = max(day_avgs.items(), key=lambda x: x[1])
    min_day = min(day_avgs.items(), key=lambda x: x[1])
    
    if max_day[1] > 3 * min_day[1]:
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        recommendations.append({
            "type": "day_distribution",
            "message": f"Your activity on {day_names[max_day[0]]} is much higher than on {day_names[min_day[0]]}. Consider a more balanced approach.",
            "priority": "low"
        })
    
    return recommendations

if __name__ == "__main__":
    # Test the smart learning module
    print("Fetching and storing actual contribution patterns...")
    success = store_actual_patterns()
    
    if success:
        print("Learning patterns from actual contributions...")
        patterns = learn_patterns()
        
        print("\nLearned Patterns:")
        for pattern_type, values in get_learned_patterns().items():
            print(f"  {pattern_type}:")
            for key, value in values.items():
                print(f"    {key}: {value}")
        
        print("\nGenerating adaptive schedule...")
        schedule = generate_adaptive_schedule(days=7)
        
        print("\nAdaptive Schedule for Next 7 Days:")
        for day in schedule:
            print(f"  {day['date']}: {day['commit_count']} commits")
            for time in day['commit_times']:
                print(f"    - {time}")
        
        print("\nContribution Trends:")
        trends = analyze_contribution_trends()
        for key, value in trends.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for subkey, subvalue in value.items():
                    print(f"    {subkey}: {subvalue}")
            else:
                print(f"  {key}: {value}")
        
        print("\nRecommendations:")
        recommendations = get_contribution_recommendations()
        for rec in recommendations:
            print(f"  [{rec['priority']}] {rec['message']}")
    else:
        print("Could not learn from actual contributions. Using default patterns.")
