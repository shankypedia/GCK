#!/bin/bash

# commit_script.sh - Main script for creating realistic GitHub contributions
# Usage: ./commit_script.sh [number_of_commits]

set -e

# Source utility functions
source "$(dirname "$0")/utils.sh"

# Get number of commits to make (default: random between 1-45)
if [ -z "$1" ]; then
  NUM_COMMITS=$(random_commit_count)
else
  NUM_COMMITS=$1
fi

echo "Will create $NUM_COMMITS commits"

# Determine if we should split commits into batches (more realistic)
SHOULD_BATCH=false
if [ $NUM_COMMITS -gt 10 ]; then
  # For larger commit counts, 70% chance to batch
  if [ $(random_number 1 10) -le 7 ]; then
    SHOULD_BATCH=true
    BATCH_COUNT=$(random_number 2 4)
    echo "Will push in $BATCH_COUNT batches for realism"
  fi
fi

# Create commits
for ((i=1; i<=$NUM_COMMITS; i++)); do
  echo "Creating commit $i of $NUM_COMMITS"
  
  # Choose a random file to modify
  FILE_TO_MODIFY=$(choose_random_file)
  echo "Selected file: $FILE_TO_MODIFY"
  
  # Modify the file
  modify_file "$FILE_TO_MODIFY"
  
  # Generate commit message
  COMMIT_MSG=$(python "$(dirname "$0")/generate_commit_message.py")
  
  # Get a realistic timestamp for the commit
  COMMIT_DATE=$(get_realistic_timestamp)
  
  # Commit with the generated date
  GIT_COMMITTER_DATE="$COMMIT_DATE" git commit --date="$COMMIT_DATE" -am "$COMMIT_MSG"
  
  # Push if this is the last commit or if we're batching and at a batch boundary
  if [ "$SHOULD_BATCH" = true ]; then
    BATCH_SIZE=$(( NUM_COMMITS / BATCH_COUNT ))
    if [ $(( i % BATCH_SIZE )) -eq 0 ] || [ $i -eq $NUM_COMMITS ]; then
      echo "Pushing batch of commits..."
      git push origin main
      
      # Sleep between batches (3-15 minutes) if not the last batch
      if [ $i -ne $NUM_COMMITS ]; then
        SLEEP_TIME=$(random_number 180 900)
        echo "Sleeping for $SLEEP_TIME seconds between batches..."
        sleep $SLEEP_TIME
      fi
    fi
  elif [ $i -eq $NUM_COMMITS ]; then
    # If not batching, push all at the end
    echo "Pushing all commits..."
    git push origin main
  fi
  
  # Sleep randomly between commits (5-300 seconds) if not the last one
  if [ $i -ne $NUM_COMMITS ]; then
    SLEEP_TIME=$(random_number 5 300)
    echo "Sleeping for $SLEEP_TIME seconds before next commit..."
    sleep $SLEEP_TIME
  fi
done

echo "Contribution process completed successfully"
