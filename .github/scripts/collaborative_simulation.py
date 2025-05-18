#!/usr/bin/env python3
"""
Collaborative Simulation for GitHub Contribution Keeper
Simulates interactions with other contributors
"""

import os
import random
import datetime
import json
from pathlib import Path

# Define collaborator profiles
COLLABORATORS = [
    {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "role": "frontend-developer",
        "activity_level": "high",  # high, medium, low
        "work_hours": {
            "start": 9,  # 9 AM
            "end": 18    # 6 PM
        },
        "timezone": "UTC-4",  # Eastern Time
        "weekend_activity": 0.2,  # Probability of weekend activity
        "preferred_files": [".js", ".html", ".css", ".jsx", ".tsx"]
    },
    {
        "name": "John Smith",
        "email": "john@example.com",
        "role": "backend-developer",
        "activity_level": "medium",
        "work_hours": {
            "start": 11,  # 11 AM
            "end": 20     # 8 PM
        },
        "timezone": "UTC+1",  # Central European Time
        "weekend_activity": 0.1,
        "preferred_files": [".py", ".js", ".sql", ".yml"]
    },
    {
        "name": "Alex Johnson",
        "email": "alex@example.com",
        "role": "devops-engineer",
        "activity_level": "medium",
        "work_hours": {
            "start": 8,   # 8 AM
            "end": 16     # 4 PM
        },
        "timezone": "UTC-7",  # Pacific Time
        "weekend_activity": 0.3,
        "preferred_files": [".yml", ".json", ".sh", ".tf", "Dockerfile"]
    },
    {
        "name": "Sam Wilson",
        "email": "sam@example.com",
        "role": "designer",
        "activity_level": "low",
        "work_hours": {
            "start": 10,  # 10 AM
            "end": 19     # 7 PM
        },
        "timezone": "UTC",
        "weekend_activity": 0.05,
        "preferred_files": [".css", ".html", ".svg", ".png"]
    }
]

# Collaboration types
COLLABORATION_TYPES = [
    {
        "type": "pull_request",
        "description": "Create a pull request for review",
        "probability": 0.4,
        "actions": ["create_branch", "commit_changes", "create_pr"]
    },
    {
        "type": "code_review",
        "description": "Review and comment on code",
        "probability": 0.3,
        "actions": ["review_code", "add_comments", "approve_pr"]
    },
    {
        "type": "pair_programming",
        "description": "Work together on code",
        "probability": 0.2,
        "actions": ["co_author_commit"]
    },
    {
        "type": "issue_discussion",
        "description": "Discuss an issue or feature",
        "probability": 0.1,
        "actions": ["create_issue", "comment_on_issue"]
    }
]

# PR and Issue templates
PR_TEMPLATES = [
    {
        "title": "Add {feature} functionality",
        "description": "This PR adds {feature} functionality to the {component} module.\n\n- Implemented {feature}\n- Added tests\n- Updated documentation",
        "labels": ["enhancement", "feature"]
    },
    {
        "title": "Fix {issue} in {component}",
        "description": "This PR fixes {issue} that was occurring in the {component} module.\n\n- Fixed {issue}\n- Added regression tests\n- Updated error handling",
        "labels": ["bug", "fix"]
    },
    {
        "title": "Refactor {component} for better performance",
        "description": "This PR refactors the {component} module to improve performance.\n\n- Optimized {specific} algorithm\n- Reduced memory usage\n- Improved error handling",
        "labels": ["refactor", "performance"]
    },
    {
        "title": "Update dependencies for {component}",
        "description": "This PR updates the dependencies for the {component} module.\n\n- Updated {dependency} to version {version}\n- Fixed compatibility issues\n- Updated documentation",
        "labels": ["dependencies", "maintenance"]
    }
]

ISSUE_TEMPLATES = [
    {
        "title": "{issue} in {component} when {action}",
        "description": "When trying to {action} in the {component} module, {issue} occurs.\n\n## Steps to reproduce\n1. Go to {component}\n2. Try to {action}\n3. Observe {issue}\n\n## Expected behavior\n{expected}\n\n## Actual behavior\n{actual}",
        "labels": ["bug"]
    },
    {
        "title": "Add {feature} to {component}",
        "description": "It would be useful to have {feature} in the {component} module.\n\n## Use case\n{use_case}\n\n## Proposed implementation\n{implementation}",
        "labels": ["enhancement", "feature-request"]
    },
    {
        "title": "Improve performance of {component}",
        "description": "The {component} module is slow when {action}.\n\n## Current performance\n{current}\n\n## Expected performance\n{expected}\n\n## Possible solutions\n{solutions}",
        "labels": ["performance"]
    },
    {
        "title": "Documentation for {feature} is unclear",
        "description": "The documentation for {feature} in {component} is unclear or incomplete.\n\n## Current documentation\n{current}\n\n## Issues\n{issues}\n\n## Suggested improvements\n{suggestions}",
        "labels": ["documentation"]
    }
]

COMMENT_TEMPLATES = [
    "I think we should consider {suggestion} for this.",
    "Have you thought about {alternative}?",
    "This looks good to me, but we might want to add {addition}.",
    "I'm concerned about {concern}. Can we address that?",
    "Great work! Just one small suggestion: {suggestion}.",
    "This implementation might cause {issue}. Maybe we should {solution}?",
    "I like the approach here. Very clean and maintainable.",
    "Let's make sure we add tests for {scenario}.",
    "The performance here might be an issue. Have you considered {optimization}?",
    "This is exactly what we needed. Nice job!"
]

# File for storing simulated collaboration data
COLLAB_DATA_PATH = Path(__file__).parent.parent / "data" / "collaboration_data.json"

def ensure_data_dir():
    """Ensure the data directory exists"""
    os.makedirs(COLLAB_DATA_PATH.parent, exist_ok=True)

def load_collaboration_data():
    """Load existing collaboration data"""
    ensure_data_dir()
    
    if COLLAB_DATA_PATH.exists():
        try:
            with open(COLLAB_DATA_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"pull_requests": [], "issues": [], "reviews": [], "pair_programming": []}
    else:
        return {"pull_requests": [], "issues": [], "reviews": [], "pair_programming": []}

def save_collaboration_data(data):
    """Save collaboration data"""
    ensure_data_dir()
    
    with open(COLLAB_DATA_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def get_random_collaborator():
    """Get a random collaborator based on activity levels"""
    # Weight collaborators by activity level
    weights = []
    for collab in COLLABORATORS:
        if collab["activity_level"] == "high":
            weights.append(3)
        elif collab["activity_level"] == "medium":
            weights.append(2)
        else:  # low
            weights.append(1)
    
    return random.choices(COLLABORATORS, weights=weights, k=1)[0]

def get_random_collaboration_type():
    """Get a random collaboration type based on probabilities"""
    types = [c["type"] for c in COLLABORATION_TYPES]
    probabilities = [c["probability"] for c in COLLABORATION_TYPES]
    
    return random.choices(types, weights=probabilities, k=1)[0]

def is_collaborator_active(collaborator, date_time):
    """Check if a collaborator would be active at the given date and time"""
    # Check if weekend
    is_weekend = date_time.weekday() >= 5  # 5=Saturday, 6=Sunday
    
    if is_weekend and random.random() > collaborator["weekend_activity"]:
        return False
    
    # Parse timezone offset
    tz_str = collaborator["timezone"]
    tz_offset = int(tz_str.replace("UTC", ""))
    
    # Adjust time to collaborator's timezone
    collab_hour = (date_time.