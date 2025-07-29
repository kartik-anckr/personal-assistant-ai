#!/usr/bin/env python3
"""
Simple Setup Script for LangGraph Beginners with Google Gemini
This helps you get everything set up quickly!
"""

import os
import subprocess
import sys

def print_step(step, message):
    """Print a step with nice formatting"""
    print(f"\n🔧 Step {step}: {message}")
    print("=" * 50)

def run_command(command, description):
    """Run a command and show the result"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e.stderr}")
        return False

def check_python():
    """Check if Python version is OK"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} - Good!")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Need Python 3.8+")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('.env.example'):
        # Copy from example
        with open('.env.example', 'r') as src, open('.env', 'w') as dst:
            dst.write(src.read())
        print("✅ Created .env file from .env.example")
        print("⚠️  Don't forget to add your Gemini API key to .env file!")
        return True
    else:
        # Create basic .env file
        env_content = """# Google Gemini API Key - Get this from Google AI Studio (https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_api_key_here

# Server Settings (optional)
PORT=8000
DEBUG=true
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created basic .env file")
        print("⚠️  Don't forget to add your Gemini API key to .env file!")
        return True

def show_api_key_instructions():
    """Show instructions for getting Gemini API key"""
    print("\n🔑 How to get your FREE Gemini API Key:")
    print("=" * 50)
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the key and paste it in your .env file")
    print("5. No credit card required - it's completely free!")

def main():
    """Main setup function"""
    print("🚀 LangGraph Setup for Beginners with Google Gemini 1.5 Flash!")
    print("This will help you get everything ready to run.")
    
    # Step 1: Check Python
    print_step(1, "Checking Python Version")
    if not check_python():
        print("Please install Python 3.8 or higher and try again.")
        return
    
    # Step 2: Install packages
    print_step(2, "Installing Python Packages")
    # Try pip3 first (for macOS), then pip
    if not run_command("pip3 install -r requirements.txt", "Installing packages with pip3"):
        if not run_command("pip install -r requirements.txt", "Installing packages with pip"):
            print("Try manually: python3 -m pip install -r requirements.txt")
            return
    
    # Step 3: Create .env file
    print_step(3, "Setting up Environment File")
    create_env_file()
    
    # Step 4: Test basic import
    print_step(4, "Testing Installation")
    try:
        import fastapi
        import langchain
        import langgraph
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ All packages imported successfully!")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Try running the install command again.")
        return
    
    # Step 5: Show API key instructions
    show_api_key_instructions()
    
    # Final instructions
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("Next steps:")
    print("1. Get your FREE Gemini API key (see instructions above)")
    print("2. Add it to the .env file")
    print("3. Run: python3 basic_agent.py (to test the agent)")
    print("4. Run: python3 main.py (to start the web server)")
    print("5. Go to: http://localhost:8000 (to see your API)")
    print("\n📚 Read tutorial.md for a detailed explanation!")
    print("🎯 Gemini 1.5 Flash is free and super fast!")
    print("\n💡 Note: Use 'python3' and 'pip3' commands on macOS/Linux")

if __name__ == "__main__":
    main() 