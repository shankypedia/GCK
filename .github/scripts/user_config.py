#!/usr/bin/env python3
"""
User configuration for GitHub Contribution Keeper
Manages user identity and activity patterns
"""

import random
import datetime

# User identity configuration
USER_NAME = "Sashank Bhamidi"
USER_EMAILS = [
    "hello@sashank.wiki",
    "sashankbhamidi@gmail.com",
    "sashank@cygenhost.com",
    "isashank@icloud.com"
]

# Project types with their specific file types
PROJECT_TYPES = [
    {
        "name": "web-app",
        "description": "Web application with frontend and backend components",
        "file_types": [".js", ".html", ".css", ".json", ".md"]
    },
    {
        "name": "api-service",
        "description": "RESTful API service",
        "file_types": [".js", ".py", ".json", ".yml", ".md"]
    },
    {
        "name": "data-analysis",
        "description": "Data analysis and visualization project",
        "file_types": [".py", ".ipynb", ".csv", ".json", ".md"]
    },
    {
        "name": "documentation",
        "description": "Documentation and knowledge base",
        "file_types": [".md", ".txt", ".html"]
    },
    {
        "name": "config-repo",
        "description": "Configuration and infrastructure repository",
        "file_types": [".yml", ".json", ".conf", ".ini", ".md"]
    }
]

# Vacation days (format: "YYYY-MM-DD")
VACATION_DAYS = [
    # Holidays
    "2023-01-01", "2023-12-25", "2023-12-31",  # New Year's, Christmas
    "2023-07-04",  # Independence Day
    "2023-11-23",  # Thanksgiving
    
    # Personal vacation (example)
    "2023-08-10", "2023-08-11", "2023-08-12", "2023-08-13", "2023-08-14",
    
    # Add more vacation days as needed
]

def get_user_name():
    """Return the user's name for Git commits"""
    return USER_NAME

def get_random_user_email():
    """Return a random email from the user's email list"""
    return random.choice(USER_EMAILS)

def get_commit_time_probability(hour):
    """Return the probability of committing at a given hour (0-23)"""
    # Higher probability during working hours
    if 9 <= hour <= 17:  # 9 AM to 5 PM
        return 0.8
    elif 7 <= hour <= 8 or 18 <= hour <= 21:  # Early morning or evening
        return 0.4
    else:  # Late night
        return 0.1

def get_commit_count_for_day(day_of_week):
    """
    Return a random number of commits based on the day of the week
    day_of_week: 0 = Monday, 6 = Sunday
    """
    # Weekdays (Monday-Friday)
    if 0 <= day_of_week <= 4:
        # Base pattern: more commits on Tuesday-Thursday, fewer on Monday/Friday
        if day_of_week in [1, 2, 3]:  # Tuesday-Thursday
            base_count = random.randint(3, 8)
        else:  # Monday, Friday
            base_count = random.randint(1, 6)
        
        # 20% chance of a very productive day
        if random.random() < 0.2:
            return base_count + random.randint(5, 15)
        # 10% chance of a very quiet day
        elif random.random() < 0.1:
            return max(1, base_count - random.randint(1, 3))
        else:
            return base_count
    
    # Weekends (Saturday-Sunday)
    else:
        # 60% chance of no commits on weekends
        if random.random() < 0.6:
            return 0
        # 30% chance of few commits
        elif random.random() < 0.3:
            return random.randint(1, 3)
        # 10% chance of normal activity
        else:
            return random.randint(2, 6)

def is_vacation_day(date_str):
    """Check if a given date is a vacation day"""
    return date_str in VACATION_DAYS

def get_random_project_type():
    """Return a random project type"""
    return random.choice(PROJECT_TYPES)

if __name__ == "__main__":
    # Test the user configuration
    print(f"User: {get_user_name()}")
    print(f"Email: {get_random_user_email()}")
    
    today = datetime.datetime.now()
    day_of_week = today.weekday()
    print(f"Today is day {day_of_week} with {get_commit_count_for_day(day_of_week)} commits")
    
    project = get_random_project_type()
    print(f"Project type: {project['name']} - {project['description']}")
