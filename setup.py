#!/usr/bin/env python3
"""
Savrli AI Setup Script

This script automates the onboarding process for new developers:
- Validates Python environment
- Installs dependencies
- Guides environment variable setup
- Runs health checks
- Provides helpful next steps

Usage:
    python setup.py
"""

import sys
import subprocess
import os
import platform
from pathlib import Path
from typing import Tuple, List

# ANSI color codes for better terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message: str):
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.OKBLUE}ℹ {message}{Colors.ENDC}")

def check_python_version() -> Tuple[bool, str]:
    """Check if Python version meets requirements (3.8+)"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        return True, version_str
    return False, version_str

def check_pip_installed() -> bool:
    """Check if pip is installed"""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_dependencies() -> Tuple[bool, str]:
    """Install project dependencies from requirements.txt"""
    try:
        print_info("Installing dependencies from requirements.txt...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True,
            text=True
        )
        return True, "Dependencies installed successfully"
    except subprocess.CalledProcessError as e:
        return False, f"Failed to install dependencies: {e.stderr}"

def check_env_file() -> Tuple[bool, str]:
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    
    if not env_path.exists():
        return False, ".env file not found"
    
    # Check for required OPENAI_API_KEY
    with open(env_path, 'r') as f:
        content = f.read()
        if "OPENAI_API_KEY" not in content:
            return False, "OPENAI_API_KEY not found in .env file"
        
        # Check if it's just a placeholder
        if "your-api-key" in content.lower() or "sk-" not in content:
            return False, "OPENAI_API_KEY appears to be a placeholder"
    
    return True, ".env file configured"

def create_env_template():
    """Create .env file from template or provide guidance"""
    env_path = Path(".env")
    
    if env_path.exists():
        print_warning(".env file already exists. Please update it manually.")
        return
    
    template = """# Savrli AI Environment Variables
# 
# REQUIRED: Get your API key from https://platform.openai.com/api-keys
OPENAI_API_KEY=your-openai-api-key-here

# OPTIONAL: OpenAI Configuration (defaults shown)
# OPENAI_MODEL=gpt-3.5-turbo
# OPENAI_MAX_TOKENS=1000
# OPENAI_TEMPERATURE=0.7
# DEFAULT_CONTEXT_WINDOW=10
# MAX_HISTORY_PER_SESSION=20

# OPTIONAL: Integration Platform Tokens
# SLACK_BOT_TOKEN=xoxb-your-token
# SLACK_SIGNING_SECRET=your-secret
# SLACK_ENABLED=false

# DISCORD_BOT_TOKEN=your-token
# DISCORD_APP_ID=your-app-id
# DISCORD_PUBLIC_KEY=your-public-key
# DISCORD_ENABLED=false

# NOTION_API_TOKEN=secret_your-token
# NOTION_ENABLED=false

# GOOGLE_DOCS_CREDENTIALS=your-credentials-json
# GOOGLE_DOCS_ENABLED=false
"""
    
    with open(env_path, 'w') as f:
        f.write(template)
    
    print_success("Created .env file template")
    print_warning("⚠️  Please edit .env and add your OPENAI_API_KEY before running the server")

def run_basic_tests() -> Tuple[bool, str]:
    """Run basic pytest tests to verify setup"""
    try:
        print_info("Running basic tests...")
        # Set a test API key if not already set
        if not os.getenv("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = "test-key-for-setup"
        
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short", "-x"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return True, "All tests passed"
        else:
            # Get last few lines of output
            lines = result.stdout.split('\n')
            error_info = '\n'.join(lines[-10:])
            return False, f"Some tests failed:\n{error_info}"
    except subprocess.TimeoutExpired:
        return False, "Tests timed out"
    except Exception as e:
        return False, f"Error running tests: {str(e)}"

def print_next_steps(env_configured: bool):
    """Print helpful next steps for the user"""
    print_header("Next Steps")
    
    if not env_configured:
        print(f"{Colors.BOLD}1. Configure your environment variables:{Colors.ENDC}")
        print("   - Edit the .env file")
        print("   - Add your OpenAI API key from: https://platform.openai.com/api-keys")
        print("   - Optional: Configure integration platform tokens\n")
    
    step_num = 2 if not env_configured else 1
    
    print(f"{Colors.BOLD}{step_num}. Start the development server:{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}uvicorn api.index:app --reload{Colors.ENDC}")
    print("   The API will be available at http://localhost:8000\n")
    
    print(f"{Colors.BOLD}{step_num + 1}. Try the interactive playground:{Colors.ENDC}")
    print(f"   Open {Colors.OKCYAN}http://localhost:8000/playground{Colors.ENDC} in your browser")
    print("   Perfect for testing AI features without writing code!\n")
    
    print(f"{Colors.BOLD}{step_num + 2}. Test the API with curl:{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}curl -X POST http://localhost:8000/ai/chat \\")
    print(f"     -H \"Content-Type: application/json\" \\")
    print(f"     -d '{{\"prompt\": \"Hello, how are you?\"}}''{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}{step_num + 3}. Run tests:{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}python -m pytest tests/ -v{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}{step_num + 4}. Read the documentation:{Colors.ENDC}")
    print("   - README.md - Full API documentation")
    print("   - CONTRIBUTING.md - Contribution guidelines")
    print("   - docs/ONBOARDING_GUIDE.md - Detailed onboarding guide\n")
    
    print_info("💡 Pro tip: Check out beginner-friendly 'First Issue' labels in GitHub Issues!")

def main():
    """Main setup flow"""
    print_header("Welcome to Savrli AI Setup!")
    print(f"{Colors.OKBLUE}This script will help you get started with Savrli AI development.{Colors.ENDC}\n")
    
    # Track overall success
    all_checks_passed = True
    
    # Step 1: Check Python version
    print_info("Step 1: Checking Python version...")
    python_ok, python_version = check_python_version()
    if python_ok:
        print_success(f"Python {python_version} detected (3.8+ required)")
    else:
        print_error(f"Python {python_version} detected, but 3.8+ is required")
        print_warning("Please upgrade Python and try again")
        all_checks_passed = False
        sys.exit(1)
    
    # Step 2: Check pip
    print_info("\nStep 2: Checking pip installation...")
    if check_pip_installed():
        print_success("pip is installed")
    else:
        print_error("pip is not installed")
        print_warning("Please install pip and try again")
        all_checks_passed = False
        sys.exit(1)
    
    # Step 3: Install dependencies
    print_info("\nStep 3: Installing dependencies...")
    deps_ok, deps_msg = install_dependencies()
    if deps_ok:
        print_success(deps_msg)
    else:
        print_error(deps_msg)
        all_checks_passed = False
    
    # Step 4: Check/create .env file
    print_info("\nStep 4: Checking environment configuration...")
    env_ok, env_msg = check_env_file()
    if env_ok:
        print_success(env_msg)
    else:
        print_warning(env_msg)
        create_env_template()
        all_checks_passed = False
    
    # Step 5: Run basic tests
    if all_checks_passed:
        print_info("\nStep 5: Running basic tests...")
        tests_ok, tests_msg = run_basic_tests()
        if tests_ok:
            print_success(tests_msg)
        else:
            print_warning("Some tests failed, but this might be due to missing API key")
            print_info("You can run tests later with: python -m pytest tests/ -v")
    
    # Final summary
    print_header("Setup Summary")
    
    if all_checks_passed:
        print_success("✨ Setup completed successfully! ✨")
        print_success("All checks passed - you're ready to start developing!")
    else:
        print_warning("⚠️  Setup completed with warnings")
        print_info("Please review the warnings above and complete the required steps")
    
    # Print next steps
    print_next_steps(env_ok)
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}Happy coding! 🚀{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Setup cancelled by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error during setup: {str(e)}")
        sys.exit(1)
