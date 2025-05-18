# GitHub Contribution Keeper

This repository contains a GitHub Actions workflow that automatically creates commits to keep your GitHub contribution graph active with realistic activity patterns.

## Features

- **Natural Commit Patterns**: Varies commit frequency based on weekdays vs weekends
- **Realistic Commit Messages**: Generates human-like commit messages
- **Varied File Changes**: Creates and modifies different types of files
- **Random Timing**: Adds natural delays between commits
- **Vacation Simulation**: Occasionally skips days to simulate time off
- **Busy Day Simulation**: Sometimes creates many commits to simulate productive days
- **Project-Type Specialization**: Generates content specific to different project types
- **Historical Backfill**: Can simulate activity dating back to July 2020
- **Personal Identity Integration**: Uses your personal information for commits

## How It Works

1. A GitHub Actions workflow runs on a scheduled basis with varied timing
2. The workflow executes Python scripts that:
   - Determine how many commits to make based on day of week and randomness
   - Generate realistic commit messages
   - Create or modify random files of various types
   - Add natural delays between commits
3. The changes are automatically pushed to the main branch

## Configuration

The workflow is configured to run at different times on weekdays and weekends:
- Weekdays: 7:17, 12:17, 16:17, and 21:17 UTC
- Weekends: 10:42, 15:42, and 19:42 UTC

You can modify the schedule by editing the cron expressions in the `.github/workflows/contribution-keeper.yml` file.

## Customization

You can customize the behavior by modifying the Python scripts in the `.github/scripts/` directory:

- `make_contribution.py`: Main script that controls the overall commit pattern
- `commit_messages.py`: Generates realistic commit messages
- `file_generator.py`: Creates and modifies various file types

### Adjustable Parameters

- Weekday vs weekend commit frequency
- Vacation day probability
- Busy day probability
- Types of files created
- Commit message patterns
- Project types and their specific content

## Personal Identity Integration

The system is configured to use your personal information for commits:
- Name: Sashank Bhamidi
- Emails: 
  - hello@sashank.wiki
  - sashankbhamidi@gmail.com
  - sashank@cygenhost.com
  - isashank@icloud.com

This ensures that all contributions are properly attributed to your GitHub account.

## Historical Backfill

The system can simulate activity dating back to July 2020, creating a comprehensive contribution history. This is useful for:
- Filling gaps in your contribution graph
- Creating a consistent activity pattern
- Demonstrating long-term project engagement

## Project Types

The system can generate content for different types of projects:
- Web applications
- API services
- Data analysis tools
- Documentation projects
- Configuration repositories

Each project type has specialized file types and content patterns that simulate real development work.

## Manual Trigger

You can also trigger the workflow manually from the "Actions" tab in your GitHub repository, with options to:
- Specify a custom number of commits
- Force the workflow to run even if the random probability would skip it
- Select a specific project type for the generated content

## Important Notes

- This project is intended for educational purposes
- Make sure this complies with GitHub's terms of service
- Consider the environmental impact of running automated workflows
