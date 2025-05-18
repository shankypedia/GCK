#!/usr/bin/env python3
"""
File generator for GitHub Contribution Keeper
Creates and modifies various file types to simulate real development work
"""

import os
import random
import string
from datetime import datetime

# File types and their extensions
FILE_TYPES = {
    "documentation": [".md", ".txt"],
    "code": [".py", ".js", ".html", ".css"],
    "data": [".json", ".csv", ".yml"],
    "config": [".ini", ".conf", ".yaml", ".env.example"]
}

# Directories to create and use for files
DIRECTORIES = [
    "docs", "src", "tests", "config", "examples", 
    "utils", "scripts", "data", "assets", "templates"
]

def ensure_directories_exist():
    """Create necessary directories if they don't exist"""
    for directory in DIRECTORIES:
        os.makedirs(directory, exist_ok=True)

def get_random_content(file_type, length=None, project_type=None):
    """Generate random content appropriate for the file type"""
    if length is None:
        length = random.randint(3, 10)  # Number of lines
    
    if file_type == ".md":
        return generate_markdown(length, project_type)
    elif file_type == ".txt":
        return generate_text(length, project_type)
    elif file_type in [".py", ".js"]:
        return generate_code(length, file_type, project_type)
    elif file_type == ".json":
        return generate_json(project_type)
    elif file_type in [".yml", ".yaml"]:
        return generate_yaml(project_type)
    else:
        return generate_text(length, project_type)

def generate_markdown(length, project_type=None):
    """Generate random markdown content"""
    headings = ["# Main Heading", "## Section", "### Subsection"]
    content = [random.choice(headings)]
    
    # Add project-specific content if available
    if project_type:
        content[0] = f"# {project_type['name'].title()} Documentation"
    
    for _ in range(length):
        options = [
            f"- List item {random.randint(1, 100)}",
            f"1. Numbered item {random.randint(1, 100)}",
            f"**Bold text** and *italic text* for emphasis",
            f"[Link text](https://example.com/{random.randint(1, 1000)})",
            f"> This is a blockquote with random text",
            f"```\nCode block\nwith multiple lines\n```",
            f"Normal paragraph with some random text."
        ]
        content.append(random.choice(options))
    
    return "\n\n".join(content)

def generate_text(length, project_type=None):
    """Generate random text content"""
    sentences = [
        "This is an example sentence.",
        "Here is another sample text.",
        "Random data for testing purposes.",
        "This file was automatically generated.",
        "Example content for demonstration.",
        "This represents placeholder text.",
        "Sample data for the project.",
        "This content is for testing only.",
        "Example file with random text.",
        "Placeholder content for the repository."
    ]
    
    # Add project-specific sentences if available
    if project_type:
        project_sentences = [
            f"This is part of the {project_type['name']} project.",
            f"Documentation for {project_type['name']} components.",
            f"Implementation details for {project_type['name']}."
        ]
        sentences.extend(project_sentences)
    
    return "\n".join(random.choices(sentences, k=length))

def generate_code(length, file_type, project_type=None):
    """Generate random code-like content"""
    if file_type == ".py":
        return generate_python_code(length, project_type)
    elif file_type == ".js":
        return generate_js_code(length, project_type)
    else:
        return generate_text(length, project_type)

def generate_python_code(length, project_type=None):
    """Generate random Python-like code"""
    # Base code structure
    code_lines = [
        "#!/usr/bin/env python3",
        "\"\"\"",
        "Example Python module",
        "\"\"\"",
        "",
        "import random",
        "import datetime",
        "",
        "def example_function():",
        "    \"\"\"Example function docstring\"\"\"",
        "    return random.randint(1, 100)",
        "",
        "class ExampleClass:",
        "    \"\"\"Example class docstring\"\"\"",
        "    ",
        "    def __init__(self):",
        "        self.value = example_function()",
        "    ",
        "    def get_value(self):",
        "        return self.value",
        "",
        "if __name__ == \"__main__\":",
        "    instance = ExampleClass()",
        "    print(f\"Value: {instance.get_value()}\")"
    ]
    
    # Customize for project type if available
    if project_type:
        project_name = project_type['name']
        code_lines[2] = f"{project_name.title()} module"
        
        # Add project-specific imports
        if project_name == "web-app":
            code_lines.insert(6, "import flask")
            code_lines.insert(7, "import json")
        elif project_name == "api-service":
            code_lines.insert(6, "import requests")
            code_lines.insert(7, "import json")
        elif project_name == "data-analysis":
            code_lines.insert(6, "import pandas as pd")
            code_lines.insert(7, "import numpy as np")
    
    # Return a subset of the code lines to vary the content
    start_idx = random.randint(0, 5)
    end_idx = min(start_idx + length + 10, len(code_lines))
    return "\n".join(code_lines[start_idx:end_idx])

def generate_js_code(length, project_type=None):
    """Generate random JavaScript-like code"""
    # Base code structure
    code_lines = [
        "/**",
        " * Example JavaScript module",
        " */",
        "",
        "// Helper function",
        "function getRandomNumber() {",
        "  return Math.floor(Math.random() * 100) + 1;",
        "}",
        "",
        "// Example class",
        "class ExampleClass {",
        "  constructor() {",
        "    this.value = getRandomNumber();",
        "  }",
        "",
        "  getValue() {",
        "    return this.value;",
        "  }",
        "}",
        "",
        "// Create an instance",
        "const instance = new ExampleClass();",
        "console.log(`Value: ${instance.getValue()}`);",
        "",
        "// Export for use in other modules",
        "export default ExampleClass;"
    ]
    
    # Customize for project type if available
    if project_type:
        project_name = project_type['name']
        code_lines[1] = f" * {project_name.title()} module"
        
        # Add project-specific code
        if project_name == "web-app":
            code_lines.insert(4, "import React from 'react';")
            code_lines.insert(5, "import { useState, useEffect } from 'react';")
        elif project_name == "api-service":
            code_lines.insert(4, "import axios from 'axios';")
            code_lines.insert(5, "const API_URL = 'https://api.example.com';")
    
    # Return a subset of the code lines to vary the content
    start_idx = random.randint(0, 5)
    end_idx = min(start_idx + length + 10, len(code_lines))
    return "\n".join(code_lines[start_idx:end_idx])

def generate_json(project_type=None):
    """Generate random JSON-like content"""
    base_json = """{
  "name": "example-project",
  "version": "1.0.0",
  "description": "Example project for demonstration",
  "main": "index.js",
  "scripts": {
    "test": "echo \\"Error: no test specified\\" && exit 1",
    "start": "node index.js"
  },
  "keywords": [
    "example",
    "demo",
    "test"
  ],
  "author": "GitHub Actions",
  "license": "MIT",
  "dependencies": {
    "example-package": "^1.0.0"
  }
}"""

    # Customize for project type if available
    if project_type:
        project_name = project_type['name']
        
        if project_name == "web-app":
            return """{
  "name": "web-application",
  "version": "1.0.0",
  "description": "Web application with modern UI",
  "main": "index.js",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^2.1.0",
    "vite": "^3.1.0"
  }
}"""
        elif project_name == "api-service":
            return """{
  "name": "api-service",
  "version": "1.0.0",
  "description": "RESTful API service",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.1",
    "mongoose": "^6.6.0",
    "cors": "^2.8.5",
    "dotenv": "^16.0.2"
  },
  "devDependencies": {
    "nodemon": "^2.0.20"
  }
}"""
        elif project_name == "data-analysis":
            return """{
  "name": "data-analysis-project",
  "version": "1.0.0",
  "description": "Data analysis and visualization",
  "main": "index.py",
  "dependencies": {
    "pandas": "^1.5.0",
    "numpy": "^1.23.3",
    "matplotlib": "^3.6.0",
    "scikit-learn": "^1.1.2"
  }
}"""
    
    return base_json

def generate_yaml(project_type=None):
    """Generate random YAML-like content"""
    base_yaml = """# Example YAML configuration
version: '3'
services:
  app:
    image: example-image:latest
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - DEBUG=false
    volumes:
      - ./data:/app/data
    restart: always

logging:
  level: info
  format: json
  
settings:
  cache: true
  timeout: 30
  retries: 3
"""

    # Customize for project type if available
    if project_type:
        project_name = project_type['name']
        
        if project_name == "web-app":
            return """# Web Application Configuration
version: '3'
services:
  frontend:
    image: node:16-alpine
    working_dir: /app
    volumes:
      - ./:/app
    ports:
      - "3000:3000"
    command: npm run dev
    environment:
      - NODE_ENV=development
      
  backend:
    image: node:16-alpine
    working_dir: /api
    volumes:
      - ./api:/api
    ports:
      - "8080:8080"
    command: npm run start
    environment:
      - NODE_ENV=development
      - DATABASE_URL=mongodb://db:27017/app
      
  db:
    image: mongo:latest
    volumes:
      - mongo-data:/data/db
    ports:
      - "27017:27017"
      
volumes:
  mongo-data:
"""
        elif project_name == "api-service":
            return """# API Service Configuration
version: '3'
services:
  api:
    build: .
    ports:
      - "4000:4000"
    environment:
      - NODE_ENV=production
      - PORT=4000
      - DATABASE_URL=postgres://user:password@db:5432/apidb
    depends_on:
      - db
      
  db:
    image: postgres:14
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=apidb
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
      
volumes:
  postgres-data:
"""
    
    return base_yaml

def create_or_modify_random_file(project_type=None):
    """Create a new file or modify an existing one with random content"""
    ensure_directories_exist()
    
    # If project type is provided, use its file types
    if project_type:
        file_extensions = project_type.get('file_types', [])
        if not file_extensions:  # Fallback if no file types specified
            file_extensions = [ext for exts in FILE_TYPES.values() for ext in exts]
    else:
        file_extensions = [ext for exts in FILE_TYPES.values() for ext in exts]
    
    # Decide whether to create a new file or modify an existing one
    if random.random() < 0.7 or not os.listdir():  # 70% new file, or if no files exist
        # Choose a random file type and directory
        extension = random.choice(file_extensions)
        directory = random.choice(DIRECTORIES)
        
        # Generate a random filename
        letters = string.ascii_lowercase
        filename = ''.join(random.choice(letters) for _ in range(8)) + extension
        filepath = os.path.join(directory, filename)
        
        # Generate content and write to file
        content = get_random_content(extension, project_type=project_type)
        with open(filepath, 'w') as f:
            f.write(content)
        
        return filepath
    else:
        # Find all files in the project
        all_files = []
        for directory in DIRECTORIES:
            if os.path.exists(directory):
                for root, _, files in os.walk(directory):
                    for file in files:
                        all_files.append(os.path.join(root, file))
        
        # If no files found, create a new one
        if not all_files:
            return create_or_modify_random_file(project_type)
        
        # Select a random file to modify
        filepath = random.choice(all_files)
        _, extension = os.path.splitext(filepath)
        
        # Read existing content
        try:
            with open(filepath, 'r') as f:
                existing_content = f.read()
        except UnicodeDecodeError:
            # If we can't read the file (e.g., binary file), create a new one instead
            return create_or_modify_random_file(project_type)
        
        # Modify the content
        if random.random() < 0.5:  # 50% chance to append
            additional_content = "\n\n# Updated on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
            additional_content += get_random_content(extension, length=2, project_type=project_type)
            new_content = existing_content + additional_content
        else:  # 50% chance to modify existing content
            lines = existing_content.split('\n')
            if len(lines) > 3:
                # Change a random line
                line_idx = random.randint(1, len(lines) - 2)
                lines[line_idx] = "# Modified: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_content = '\n'.join(lines)
            else:
                # File too short, just append
                new_content = existing_content + "\n\n# Updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Write the modified content back to the file
        with open(filepath, 'w') as f:
            f.write(new_content)
        
        return filepath

if __name__ == "__main__":
    # Test the file generator
    filepath = create_or_modify_random_file()
    print(f"Created/modified file: {filepath}")
