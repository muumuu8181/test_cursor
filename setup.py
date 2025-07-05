#!/usr/bin/env python3
"""
Setup script for Twitter Auto Poster
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def create_env_file():
    """Create .env file from template"""
    if Path(".env").exists():
        print("⚠️  .env file already exists, skipping creation")
        return True
    
    if Path(".env.example").exists():
        return run_command("cp .env.example .env", "Creating .env file")
    else:
        print("❌ .env.example file not found")
        return False

def create_posts_folder():
    """Create posts folder"""
    posts_folder = Path("posts")
    if posts_folder.exists():
        print("⚠️  posts folder already exists")
        return True
    
    try:
        posts_folder.mkdir(exist_ok=True)
        print("✅ Created posts folder")
        return True
    except Exception as e:
        print(f"❌ Failed to create posts folder: {e}")
        return False

def create_example_post():
    """Create an example post"""
    from datetime import datetime, timedelta
    
    # Create example post for tomorrow at 9 AM
    tomorrow = datetime.now() + timedelta(days=1)
    folder_name = tomorrow.strftime("%Y-%m-%d_09-00")
    
    return run_command(f"python main.py --create-example {folder_name}", 
                      f"Creating example post for {folder_name}")

def test_system():
    """Test the system"""
    print("\n🧪 Testing system...")
    print("⚠️  Make sure to configure your Twitter API keys in .env file before running tests")
    
    choice = input("Do you want to run the system test now? (y/N): ").strip().lower()
    if choice in ['y', 'yes']:
        return run_command("python main.py --test", "Running system test")
    else:
        print("⏭️  Skipping system test")
        return True

def main():
    """Main setup function"""
    print("🚀 Setting up Twitter Auto Poster...")
    print("=" * 50)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Installing dependencies", install_dependencies),
        ("Creating .env file", create_env_file),
        ("Creating posts folder", create_posts_folder),
        ("Creating example post", create_example_post),
        ("Testing system", test_system),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        if not step_func():
            failed_steps.append(step_name)
    
    print("\n" + "=" * 50)
    
    if failed_steps:
        print("❌ Setup completed with errors:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\n📋 Next steps:")
        print("   1. Fix the errors above")
        print("   2. Configure your Twitter API keys in .env file")
        print("   3. Run: python main.py --test")
    else:
        print("✅ Setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Configure your Twitter API keys in .env file")
        print("   2. Add your image to the example post folder")
        print("   3. Edit the message.txt file in the example post folder")
        print("   4. Run: python main.py --test")
        print("   5. Run: python main.py --start")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()