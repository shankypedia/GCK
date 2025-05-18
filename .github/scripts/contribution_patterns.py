#!/usr/bin/env python3
"""
Contribution Patterns for GitHub Contribution Keeper
Implements advanced patterns for more realistic contribution simulation
"""

import random
import datetime
from dateutil.relativedelta import relativedelta

# Define seasons of activity
SEASONS = {
    "high_intensity": {
        "description": "Period of intense activity (e.g., project deadline, hackathon)",
        "duration_days": (3, 14),  # Min and max duration in days
        "commit_multiplier": (1.5, 3.0),  # Multiply normal commit count by this factor
        "probability": 0.15  # Probability of starting a high intensity season on any given day
    },
    "normal": {
        "description": "Regular activity pattern",
        "duration_days": (14, 60),
        "commit_multiplier": (0.8, 1.2),
        "probability": 0.6
    },
    "low_intensity": {
        "description": "Period of reduced activity (e.g., between projects, light workload)",
        "duration_days": (5, 21),
        "commit_multiplier": (0.3, 0.7),
        "probability": 0.25
    },
    "break": {
        "description": "Break from coding (e.g., vacation, personal time)",
        "duration_days": (1, 7),
        "commit_multiplier": (0.0, 0.1),  # Almost no commits
        "probability": 0.1
    }
}

# Project focus periods - simulates working on specific projects for extended periods
PROJECT_FOCUS = {
    "duration_days": (7, 30),  # Focus on a project for 1-4 weeks
    "transition_days": (1, 3),  # Days with mixed project types during transition
    "probability_change": 0.2  # Probability of changing focus on any given day
}

# Collaboration patterns
COLLABORATION_PATTERNS = {
    "pull_request_review": {
        "description": "Days where you primarily review PRs rather than commit",
        "commit_multiplier": (0.3, 0.6),  # Fewer commits on PR review days
        "duration_days": (1, 2),
        "probability": 0.15
    },
    "pair_programming": {
        "description": "Days where commits are made with co-authors",
        "commit_multiplier": (0.7, 1.0),
        "duration_days": (1, 3),
        "probability": 0.1,
        "co_authors": [
            "Jane Doe <jane@example.com>",
            "John Smith <john@example.com>",
            "Alex Johnson <alex@example.com>",
            "Sam Wilson <sam@example.com>"
        ]
    }
}

# Time-based patterns (e.g., time of year)
TIME_PATTERNS = {
    # Month-based patterns (1=January, 12=December)
    "monthly": {
        1: 0.9,   # January: Slightly reduced (new year)
        2: 1.0,   # February: Normal
        3: 1.1,   # March: Slightly increased
        4: 1.0,   # April: Normal
        5: 1.0,   # May: Normal
        6: 0.8,   # June: Reduced (summer begins)
        7: 0.7,   # July: More reduced (summer)
        8: 0.7,   # August: More reduced (summer)
        9: 1.2,   # September: Increased (back to work)
        10: 1.1,  # October: Slightly increased
        11: 1.0,  # November: Normal
        12: 0.8   # December: Reduced (holidays)
    },
    
    # Special periods
    "special_periods": [
        {
            "name": "End of Quarter",
            "months": [3, 6, 9, 12],
            "days": list(range(25, 32)),  # Last week of quarter
            "multiplier": 1.4  # 40% more commits
        },
        {
            "name": "Start of Year",
            "months": [1],
            "days": list(range(1, 15)),  # First two weeks
            "multiplier": 1.3  # 30% more commits
        }
    ]
}

class ContributionPattern:
    def __init__(self, start_date=None):
        """Initialize the contribution pattern tracker"""
        self.start_date = start_date or datetime.datetime.now()
        self.current_date = self.start_date
        
        # Initialize current season
        self.current_season = self._select_random_season()
        self.season_end_date = self._calculate_season_end_date(self.current_season)
        
        # Initialize current project focus
        self.current_project_focus = self._select_random_project()
        self.project_focus_end_date = self._calculate_project_end_date()
        
        # Initialize collaboration state
        self.current_collaboration = None
        self.collaboration_end_date = None
        
        # Track pattern history
        self.pattern_history = []
    
    def _select_random_season(self):
        """Select a random season based on probabilities"""
        seasons = list(SEASONS.keys())
        probabilities = [SEASONS[s]["probability"] for s in seasons]
        
        # Normalize probabilities to sum to 1
        total = sum(probabilities)
        normalized_probs = [p/total for p in probabilities]
        
        return random.choices(seasons, weights=normalized_probs, k=1)[0]
    
    def _calculate_season_end_date(self, season):
        """Calculate when the current season ends"""
        min_days, max_days = SEASONS[season]["duration_days"]
        duration = random.randint(min_days, max_days)
        return self.current_date + datetime.timedelta(days=duration)
    
    def _select_random_project(self):
        """Select a random project type"""
        from user_config import get_random_project_type
        return get_random_project_type()
    
    def _calculate_project_end_date(self):
        """Calculate when the current project focus ends"""
        min_days, max_days = PROJECT_FOCUS["duration_days"]
        duration = random.randint(min_days, max_days)
        return self.current_date + datetime.timedelta(days=duration)
    
    def _select_random_collaboration(self):
        """Select a random collaboration pattern or None"""
        # 70% chance of no collaboration
        if random.random() < 0.7:
            return None
            
        patterns = list(COLLABORATION_PATTERNS.keys())
        probabilities = [COLLABORATION_PATTERNS[p]["probability"] for p in patterns]
        
        # Normalize probabilities
        total = sum(probabilities)
        if total == 0:
            return None
            
        normalized_probs = [p/total for p in probabilities]
        
        selected = random.choices(patterns, weights=normalized_probs, k=1)[0]
        
        # Calculate end date for collaboration
        min_days, max_days = COLLABORATION_PATTERNS[selected]["duration_days"]
        duration = random.randint(min_days, max_days)
        self.collaboration_end_date = self.current_date + datetime.timedelta(days=duration)
        
        return selected
    
    def get_pattern_for_date(self, date=None):
        """Get the contribution pattern for a specific date"""
        if date is None:
            date = self.current_date
        
        # Update internal state if we're advancing time
        if date > self.current_date:
            self._advance_to_date(date)
        
        # Calculate commit multiplier based on current season
        season_min, season_max = SEASONS[self.current_season]["commit_multiplier"]
        season_multiplier = random.uniform(season_min, season_max)
        
        # Apply monthly pattern
        month = date.month
        month_multiplier = TIME_PATTERNS["monthly"].get(month, 1.0)
        
        # Check for special periods
        special_multiplier = 1.0
        for period in TIME_PATTERNS["special_periods"]:
            if date.month in period["months"] and date.day in period["days"]:
                special_multiplier = period["multiplier"]
                break
        
        # Apply collaboration pattern if active
        collab_multiplier = 1.0
        co_author = None
        if self.current_collaboration:
            collab_min, collab_max = COLLABORATION_PATTERNS[self.current_collaboration]["commit_multiplier"]
            collab_multiplier = random.uniform(collab_min, collab_max)
            
            # If pair programming, select a co-author
            if self.current_collaboration == "pair_programming":
                co_authors = COLLABORATION_PATTERNS["pair_programming"]["co_authors"]
                co_author = random.choice(co_authors)
        
        # Calculate final multiplier
        final_multiplier = season_multiplier * month_multiplier * special_multiplier * collab_multiplier
        
        # Create pattern data
        pattern = {
            "date": date.strftime("%Y-%m-%d"),
            "season": self.current_season,
            "project_focus": self.current_project_focus,
            "collaboration": self.current_collaboration,
            "co_author": co_author,
            "commit_multiplier": final_multiplier,
            "description": self._generate_pattern_description(date)
        }
        
        # Add to history
        self.pattern_history.append(pattern)
        
        return pattern
    
    def _advance_to_date(self, target_date):
        """Advance the internal state to the target date"""
        while self.current_date < target_date:
            self.current_date += datetime.timedelta(days=1)
            
            # Check if season has ended
            if self.current_date >= self.season_end_date:
                self.current_season = self._select_random_season()
                self.season_end_date = self._calculate_season_end_date(self.current_season)
            
            # Check if project focus has ended
            if self.current_date >= self.project_focus_end_date:
                # Chance to change project focus
                if random.random() < PROJECT_FOCUS["probability_change"]:
                    self.current_project_focus = self._select_random_project()
                    self.project_focus_end_date = self._calculate_project_end_date()
            
            # Check if collaboration has ended or should start
            if self.current_collaboration and self.current_date >= self.collaboration_end_date:
                self.current_collaboration = None
            elif not self.current_collaboration and random.random() < 0.1:  # 10% daily chance
                self.current_collaboration = self._select_random_collaboration()
    
    def _generate_pattern_description(self, date):
        """Generate a human-readable description of the current pattern"""
        descriptions = []
        
        # Season description
        descriptions.append(f"{self.current_season.replace('_', ' ').title()} season")
        
        # Project focus
        descriptions.append(f"Working on {self.current_project_focus['name']}")
        
        # Collaboration
        if self.current_collaboration:
            collab_desc = COLLABORATION_PATTERNS[self.current_collaboration]["description"]
            descriptions.append(collab_desc)
        
        # Special period
        for period in TIME_PATTERNS["special_periods"]:
            if date.month in period["months"] and date.day in period["days"]:
                descriptions.append(period["name"])
                break
        
        return " | ".join(descriptions)
    
    def get_commit_count(self, base_count, date=None):
        """Get the adjusted commit count based on patterns"""
        pattern = self.get_pattern_for_date(date)
        multiplier = pattern["commit_multiplier"]
        
        # Apply multiplier and round to nearest integer
        adjusted_count = round(base_count * multiplier)
        
        # Ensure at least 0 commits
        return max(0, adjusted_count)
    
    def get_project_focus(self, date=None):
        """Get the current project focus"""
        pattern = self.get_pattern_for_date(date)
        return pattern["project_focus"]
    
    def get_co_author(self, date=None):
        """Get co-author for the current date if pair programming"""
        pattern = self.get_pattern_for_date(date)
        return pattern.get("co_author")
    
    def generate_report(self, start_date=None, end_date=None):
        """Generate a report of contribution patterns for a date range"""
        if start_date is None:
            start_date = self.start_date
        if end_date is None:
            end_date = self.current_date
        
        report = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "patterns": []
        }
        
        current = start_date
        while current <= end_date:
            pattern = self.get_pattern_for_date(current)
            report["patterns"].append(pattern)
            current += datetime.timedelta(days=1)
        
        return report

if __name__ == "__main__":
    # Test the contribution pattern system
    pattern_tracker = ContributionPattern()
    
    # Get pattern for today
    today = datetime.datetime.now()
    pattern = pattern_tracker.get_pattern_for_date(today)
    print(f"Pattern for {today.strftime('%Y-%m-%d')}:")
    print(f"  Season: {pattern['season']}")
    print(f"  Project: {pattern['project_focus']['name']}")
    print(f"  Collaboration: {pattern['collaboration']}")
    print(f"  Multiplier: {pattern['commit_multiplier']:.2f}")
    print(f"  Description: {pattern['description']}")
    
    # Test commit count adjustment
    base_count = 5
    adjusted_count = pattern_tracker.get_commit_count(base_count)
    print(f"Base commit count: {base_count}, Adjusted: {adjusted_count}")
