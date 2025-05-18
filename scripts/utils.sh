#!/bin/bash

# utils.sh - Utility functions for GitHub contribution scripts

# Generate a random number between min and max (inclusive)
random_number() {
  local min=$1
  local max=$2
  echo $(( $min + RANDOM % ($max - $min + 1) ))
}

# Generate a random commit count based on day of week
random_commit_count() {
  local day_of_week=$(date +%u)  # 1=Monday, 7=Sunday
  
  # Weekdays (Monday-Friday)
  if [ $day_of_week -le 5 ]; then
    # Base pattern: more commits on Tuesday-Thursday, fewer on Monday/Friday
    if [ $day_of_week -ge 2 ] && [ $day_of_week -le 4 ]; then
      # Tuesday-Thursday
      base_count=$(random_number 3 8)
    else
      # Monday, Friday
      base_count=$(random_number 1 6)
    fi
    
    # 20% chance of a very productive day
    if [ $(random_number 1 100) -le 20 ]; then
      echo $(( $base_count + $(random_number 5 15) ))
    # 10% chance of a very quiet day
    elif [ $(random_number 1 100) -le 10 ]; then
      echo $(( $base_count - $(random_number 0 2) ))
    else
      echo $base_count
    fi
  
  # Weekends (Saturday-Sunday)
  else
    # 60% chance of no commits on weekends
    if [ $(random_number 1 100) -le 60 ]; then
      echo 0
    # 30% chance of few commits
    elif [ $(random_number 1 100) -le 30 ]; then
      echo $(random_number 1 3)
    # 10% chance of normal activity
    else
      echo $(random_number 2 6)
    fi
  fi
}

# Choose a random file to modify
choose_random_file() {
  # Define directories to look in
  local dirs=("docs" "src" "tests" "config" "examples" "utils" "scripts" "data" "assets" "templates")
  
  # Create directories if they don't exist
  for dir in "${dirs[@]}"; do
    mkdir -p "$dir"
  done
  
  # Choose a random directory
  local dir=${dirs[$(random_number 0 $((${#dirs[@]} - 1)))]}
  
  # Check if directory has files
  local file_count=$(ls -1 "$dir" 2>/dev/null | wc -l)
  
  if [ "$file_count" -eq 0 ]; then
    # No files, create a new one
    local extensions=(".md" ".txt" ".py" ".js" ".json" ".yml" ".html" ".css")
    local ext=${extensions[$(random_number 0 $((${#extensions[@]} - 1)))]}
    local filename="file_$(date +%s)$ext"
    touch "$dir/$filename"
    echo "$dir/$filename"
  else
    # Choose a random existing file
    local files=($(ls -1 "$dir"))
    local file=${files[$(random_number 0 $((${#files[@]} - 1)))]}
    echo "$dir/$file"
  fi
}

# Modify a file with random content
modify_file() {
  local file="$1"
  local ext="${file##*.}"
  
  # Get current date and time
  local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
  
  # Append content based on file type
  case "$ext" in
    md|txt)
      echo -e "\n\n## Updated on $timestamp\n\nThis is an automatic update." >> "$file"
      ;;
    py)
      echo -e "\n\n# Updated on $timestamp\ndef updated_function():\n    return 'This is an automatic update'" >> "$file"
      ;;
    js)
      echo -e "\n\n// Updated on $timestamp\nfunction updatedFunction() {\n    return 'This is an automatic update';\n}" >> "$file"
      ;;
    json)
      # For JSON files, we need to be careful with the structure
      # This assumes a simple JSON object with a closing }
      sed -i '$ d' "$file"  # Remove last line (closing brace)
      echo -e "  \"lastUpdated\": \"$timestamp\"\n}" >> "$file"
      ;;
    yml|yaml)
      echo -e "\n# Updated on $timestamp\nlastUpdated: \"$timestamp\"" >> "$file"
      ;;
    html)
      echo -e "\n<!-- Updated on $timestamp -->\n<div>This is an automatic update.</div>" >> "$file"
      ;;
    css)
      echo -e "\n/* Updated on $timestamp */\n.updated {\n  color: #333;\n  font-weight: bold;\n}" >> "$file"
      ;;
    *)
      echo -e "\n\n# Updated on $timestamp\nThis is an automatic update." >> "$file"
      ;;
  esac
}

# Get a realistic timestamp for commits
get_realistic_timestamp() {
  # Get current date
  local date=$(date "+%Y-%m-%d")
  
  # Generate a random time during working hours
  local hour=$(random_number 9 17)
  local minute=$(random_number 0 59)
  local second=$(random_number 0 59)
  
  echo "$date $hour:$minute:$second"
}
