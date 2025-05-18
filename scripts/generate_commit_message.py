#!/usr/bin/env python3

"""
generate_commit_message.py - Generate realistic commit messages

This script produces human-like commit messages by randomly selecting from
predefined templates and combining them with appropriate context.
"""

import random
import sys
from datetime import datetime

# Define commit message themes
THEMES = {
    "feature": [
        "Add {feature}",
        "Implement {feature}",
        "Create {feature}",
        "Introduce {feature}",
        "Build {feature}"
    ],
    "bugfix": [
        "Fix {issue}",
        "Resolve {issue}",
        "Fix bug in {component}",
        "Patch {issue}",
        "Correct {issue}"
    ],
    "refactor": [
        "Refactor {component}",
        "Clean up {component}",
        "Simplify {component}",
        "Restructure {component}",
        "Optimize {component}"
    ],
    "docs": [
        "Update documentation for {component}",
        "Improve {component} docs",
        "Add docs for {component}",
        "Document {feature}",
        "Fix typo in {component} documentation"
    ],
    "style": [
        "Format {component}",
        "Fix whitespace in {component}",
        "Style improvements in {component}",
        "Lint {component}",
        "Standardize code style in {component}"
    ],
    "chore": [
        "Update dependencies",
        "Bump version",
        "Update config files",
        "Maintenance tasks",
        "Housekeeping"
    ]
}

# Components that might appear in commit messages
COMPONENTS = [
    "utils module",
    "config parser",
    "data processor",
    "authentication system",
    "API client",
    "database connector",
    "logger",
    "UI components",
    "test suite",
    "build system",
    "documentation",
    "error handling",
    "validation logic",
    "helper functions",
    "core functionality"
]

# Features that might be implemented
FEATURES = [
    "user authentication",
    "data export functionality",
    "caching mechanism",
    "new API endpoint",
    "dark mode",
    "search functionality",
    "notification system",
    "analytics dashboard",
    "user preferences",
    "backup system",
    "rate limiting",
    "error reporting",
    "performance monitoring",
    "keyboard shortcuts",
    "mobile responsiveness"
]

# Issues that might be fixed
ISSUES = [
    "memory leak",
    "race condition",
    "edge case in validation",
    "incorrect error message",
    "performance bottleneck",
    "security vulnerability",
    "broken link",
    "incorrect calculation",
    "timeout issue",
    "compatibility problem",
    "crash on startup",
    "data corruption issue",
    "UI glitch",
    "incorrect sorting",
    "connection handling"
]

def generate_commit_message():
    """Generate a realistic commit message"""
    # Select a random theme with weighted probability
    theme_weights = {
        "feature": 20,
        "bugfix": 30,
        "refactor": 20,
        "docs": 15,
        "style": 10,
        "chore": 5
    }
    
    themes = list(theme_weights.keys())
    weights = list(theme_weights.values())
    
    selected_theme = random.choices(themes, weights=weights, k=1)[0]
    
    # Select a template from the chosen theme
    template = random.choice(THEMES[selected_theme])
    
    # Fill in the template with appropriate content
    if "{component}" in template:
        component = random.choice(COMPONENTS)
        message = template.replace("{component}", component)
    elif "{feature}" in template:
        feature = random.choice(FEATURES)
        message = template.replace("{feature}", feature)
    elif "{issue}" in template:
        issue = random.choice(ISSUES)
        message = template.replace("{issue}", issue)
    else:
        message = template
    
    # 20% chance to add a scope prefix
    if random.random() < 0.2:
        scope = random.choice(["core", "ui", "api", "docs", "tests", "build", "ci"])
        message = f"{scope}: {message}"
    
    # 10% chance to add a longer description
    if random.random() < 0.1:
        descriptions = [
            "This resolves the issues we've been seeing in production.",
            "Closes #123.",
            "Part of the Q3 improvements initiative.",
            "This should improve performance significantly.",
            "Based on user feedback from the beta test."
        ]
        message += "\n\n" + random.choice(descriptions)
    
    return message

if __name__ == "__main__":
    print(generate_commit_message())
