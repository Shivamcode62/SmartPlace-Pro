#!/usr/bin/env python3
"""
Setup script for SmartPlace Pro
Run this first to initialize the project
"""

import os
import sys
import subprocess

def setup_project():
    """Setup the project"""
    print("🔧 Setting up SmartPlace Pro...")
    
    # Create virtual environment
    print("\n📦 Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # Activate virtual environment and install dependencies
    print("\n📥 Installing dependencies...")
    if sys.platform == "win32":
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"
    
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    
    # Create directories
    directories = ['data', 'static/images', 'static/js', 'frontend/css', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    print("\n✅ Setup complete! Run 'python run.py' to start the application.")

if __name__ == "__main__":
    setup_project()