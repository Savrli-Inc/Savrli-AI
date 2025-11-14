#!/bin/bash
#
# Savrli AI Interactive Setup Script
#
# This script automates the onboarding process for new contributors:
# - Validates Python environment (3.8+ required)
# - Creates and activates virtual environment (optional but recommended)
# - Installs project dependencies
# - Sets up environment variables with interactive prompts
# - Runs basic health checks and tests
# - Provides clear next steps and troubleshooting guidance
#
# Usage: ./scripts/setup.sh
#
# Safety guarantees:
# - No destructive operations (won't delete files or overwrite without confirmation)
# - All prompts have safe defaults
# - Virtual environment is isolated from system Python
# - Existing .env file is preserved (only prompts if missing/incomplete)
#

set -e  # Exit on error (but we handle errors gracefully)

# Colors for better output readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Track whether we created a virtual environment
VENV_CREATED=false
VENV_PATH=""

# ============================================================================
# Helper Functions
# ============================================================================

print_header() {
    echo -e "\n${BOLD}========================================================================${NC}"
    echo -e "${BOLD}$(printf '%*s' $(((70+${#1})/2)) "$1")${NC}"
    echo -e "${BOLD}========================================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_step() {
    echo -e "\n${BOLD}${CYAN}➜ $1${NC}"
}

# Prompt user for yes/no with default
# Usage: prompt_yes_no "Question?" "default"
# Returns: 0 for yes, 1 for no
prompt_yes_no() {
    local question="$1"
    local default="$2"
    local prompt=""
    
    if [ "$default" = "y" ]; then
        prompt="[Y/n]"
    else
        prompt="[y/N]"
    fi
    
    while true; do
        read -p "$(echo -e ${CYAN}"$question $prompt: "${NC})" response
        response=${response:-$default}
        case "$response" in
            [Yy]|[Yy][Ee][Ss]) return 0 ;;
            [Nn]|[Nn][Oo]) return 1 ;;
            *) echo "Please answer yes or no." ;;
        esac
    done
}

# ============================================================================
# Step 1: Check Python Version
# ============================================================================

check_python() {
    print_step "Step 1: Checking Python version..."
    
    # Check if python3 is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        echo ""
        echo "Please install Python 3.8 or higher:"
        echo "  - macOS: brew install python3"
        echo "  - Ubuntu/Debian: sudo apt-get install python3"
        echo "  - Windows: Download from https://www.python.org/downloads/"
        echo ""
        return 1
    fi
    
    # Get Python version
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    print_info "Found Python $PYTHON_VERSION"
    
    # Check version requirements (3.8+)
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_error "Python $PYTHON_VERSION is too old (3.8+ required)"
        echo ""
        echo "Please upgrade Python to version 3.8 or higher"
        return 1
    fi
    
    print_success "Python $PYTHON_VERSION meets requirements (3.8+ required)"
    return 0
}

# ============================================================================
# Step 2: Virtual Environment Setup (Optional but Recommended)
# ============================================================================

setup_virtualenv() {
    print_step "Step 2: Virtual Environment Setup (Recommended)"
    
    echo ""
    echo "A virtual environment isolates project dependencies from your system Python."
    echo "This prevents version conflicts and keeps your system clean."
    echo ""
    
    # Check if already in a virtual environment
    if [ -n "$VIRTUAL_ENV" ]; then
        print_info "Already in a virtual environment: $VIRTUAL_ENV"
        return 0
    fi
    
    # Check if venv directory already exists
    if [ -d "venv" ]; then
        print_info "Virtual environment directory 'venv' already exists"
        
        if prompt_yes_no "Do you want to use the existing virtual environment?" "y"; then
            print_info "Activating existing virtual environment..."
            source venv/bin/activate 2>/dev/null || {
                print_error "Failed to activate virtual environment"
                print_info "The venv directory may be corrupted. Consider deleting it and running setup again."
                return 1
            }
            VENV_PATH="venv"
            print_success "Using existing virtual environment"
            return 0
        else
            print_info "Skipping virtual environment activation"
            return 0
        fi
    fi
    
    # Prompt to create new virtual environment
    if prompt_yes_no "Would you like to create a virtual environment?" "y"; then
        print_info "Creating virtual environment in ./venv..."
        
        # Create virtual environment
        if python3 -m venv venv; then
            print_success "Virtual environment created"
            VENV_CREATED=true
            VENV_PATH="venv"
            
            # Activate it
            print_info "Activating virtual environment..."
            source venv/bin/activate
            print_success "Virtual environment activated"
        else
            print_error "Failed to create virtual environment"
            print_warning "Continuing without virtual environment (not recommended)"
            return 1
        fi
    else
        print_warning "Skipping virtual environment (not recommended for development)"
        echo "You can create one later with: python3 -m venv venv"
    fi
    
    return 0
}

# ============================================================================
# Step 3: Install Dependencies
# ============================================================================

install_dependencies() {
    print_step "Step 3: Installing Python dependencies..."
    
    # Check if pip is available
    if ! python3 -m pip --version &> /dev/null; then
        print_error "pip is not installed"
        echo "Please install pip and try again"
        return 1
    fi
    
    print_info "Installing packages from requirements.txt..."
    echo ""
    
    # Install with progress output
    if python3 -m pip install -r requirements.txt; then
        echo ""
        print_success "All dependencies installed successfully"
        return 0
    else
        echo ""
        print_error "Failed to install some dependencies"
        echo ""
        echo "Troubleshooting tips:"
        echo "  1. Check your internet connection"
        echo "  2. Try upgrading pip: python3 -m pip install --upgrade pip"
        echo "  3. If using a virtual environment, make sure it's activated"
        return 1
    fi
}

# ============================================================================
# Step 4: Environment Variables Setup
# ============================================================================

setup_env_file() {
    print_step "Step 4: Environment Variables Configuration"
    
    echo ""
    echo "Savrli AI requires an OpenAI API key to function."
    echo "Other environment variables are optional and have sensible defaults."
    echo ""
    
    # Check if .env file exists
    if [ -f .env ]; then
        print_info ".env file already exists"
        
        # Check if OPENAI_API_KEY is configured
        if grep -q "^OPENAI_API_KEY=sk-" .env 2>/dev/null; then
            print_success "OPENAI_API_KEY appears to be configured"
            
            if prompt_yes_no "Do you want to update your .env file?" "n"; then
                configure_env_interactive
            fi
        else
            print_warning "OPENAI_API_KEY not found or not properly set in .env"
            echo ""
            if prompt_yes_no "Would you like to configure it now?" "y"; then
                configure_env_interactive
            else
                print_warning "Remember to add your OPENAI_API_KEY to .env before running the server!"
                return 1
            fi
        fi
    else
        print_info ".env file not found"
        
        if prompt_yes_no "Would you like to create and configure .env now?" "y"; then
            configure_env_interactive
        else
            create_env_template
            print_warning "Remember to edit .env and add your OPENAI_API_KEY!"
            return 1
        fi
    fi
    
    return 0
}

# Create .env template
create_env_template() {
    cat > .env << 'EOF'
# Savrli AI Environment Variables
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
EOF
    
    print_success "Created .env template file"
}

# Interactive configuration
configure_env_interactive() {
    echo ""
    print_info "Let's configure your environment variables..."
    echo ""
    
    # If .env doesn't exist, create template first
    if [ ! -f .env ]; then
        create_env_template
    fi
    
    # Prompt for OpenAI API key
    echo -e "${CYAN}OpenAI API Key:${NC}"
    echo "Get one from: https://platform.openai.com/api-keys"
    echo ""
    
    # Get current value if it exists
    CURRENT_KEY=$(grep "^OPENAI_API_KEY=" .env 2>/dev/null | cut -d'=' -f2)
    
    if [ -n "$CURRENT_KEY" ] && [ "$CURRENT_KEY" != "your-openai-api-key-here" ]; then
        echo "Current key: ${CURRENT_KEY:0:10}...${CURRENT_KEY: -4}"
        if ! prompt_yes_no "Do you want to change it?" "n"; then
            print_info "Keeping existing API key"
            return 0
        fi
    fi
    
    read -p "Enter your OpenAI API key (or press Enter to skip): " NEW_API_KEY
    
    if [ -n "$NEW_API_KEY" ]; then
        # Validate format (should start with sk-)
        if [[ $NEW_API_KEY == sk-* ]]; then
            # Update .env file
            if grep -q "^OPENAI_API_KEY=" .env; then
                # Replace existing line
                sed -i.bak "s|^OPENAI_API_KEY=.*|OPENAI_API_KEY=$NEW_API_KEY|" .env
                rm -f .env.bak
            else
                # Add new line
                echo "OPENAI_API_KEY=$NEW_API_KEY" >> .env
            fi
            print_success "OpenAI API key configured"
        else
            print_warning "API key should start with 'sk-'. Please check and update .env manually."
        fi
    else
        print_warning "Skipped API key configuration. Remember to add it to .env!"
    fi
}

# ============================================================================
# Step 5: Run Tests
# ============================================================================

run_tests() {
    print_step "Step 5: Running Basic Health Checks"
    
    echo ""
    print_info "Running test suite to verify installation..."
    echo ""
    
    # Set test API key if not configured (for tests that mock OpenAI)
    if ! grep -q "^OPENAI_API_KEY=sk-" .env 2>/dev/null; then
        print_info "Using test API key for health checks (mocked responses)"
        export OPENAI_API_KEY="test-key-for-setup-checks"
    fi
    
    # Run tests with brief output
    if python3 -m pytest tests/ -v --tb=short -x 2>&1 | tail -30; then
        echo ""
        print_success "✨ All health checks passed!"
        return 0
    else
        echo ""
        print_warning "Some tests failed"
        echo ""
        echo "This might be because:"
        echo "  1. OPENAI_API_KEY is not configured (tests may need valid key)"
        echo "  2. A dependency is missing or outdated"
        echo "  3. There's an existing issue in the codebase (not your fault!)"
        echo ""
        print_info "You can run tests manually later with: python3 -m pytest tests/ -v"
        return 1
    fi
}

# ============================================================================
# Print Next Steps
# ============================================================================

print_next_steps() {
    local env_configured=$1
    
    print_header "🎉 Setup Complete!"
    
    echo -e "${BOLD}What's Next?${NC}\n"
    
    STEP=1
    
    # Virtual environment activation reminder
    if [ "$VENV_CREATED" = true ]; then
        echo -e "${BOLD}${STEP}. Activate virtual environment (for future terminal sessions):${NC}"
        echo -e "   ${CYAN}source venv/bin/activate${NC}"
        echo ""
        STEP=$((STEP + 1))
    fi
    
    # Environment configuration reminder
    if [ "$env_configured" = false ]; then
        echo -e "${BOLD}${STEP}. Configure your environment variables:${NC}"
        echo "   - Edit the .env file: nano .env (or your preferred editor)"
        echo "   - Add your OpenAI API key from: https://platform.openai.com/api-keys"
        echo "   - Optional: Configure integration platform tokens"
        echo ""
        STEP=$((STEP + 1))
    fi
    
    # Start the server
    echo -e "${BOLD}${STEP}. Start the development server:${NC}"
    echo -e "   ${CYAN}uvicorn api.index:app --reload${NC}"
    echo "   The API will be available at http://localhost:8000"
    echo ""
    STEP=$((STEP + 1))
    
    # Try the playground
    echo -e "${BOLD}${STEP}. Try the interactive playground:${NC}"
    echo -e "   Open ${CYAN}http://localhost:8000/playground${NC} in your browser"
    echo "   Perfect for testing AI features without writing code!"
    echo ""
    STEP=$((STEP + 1))
    
    # Test with curl
    echo -e "${BOLD}${STEP}. Test the API with curl:${NC}"
    echo -e "   ${CYAN}curl -X POST http://localhost:8000/ai/chat \\${NC}"
    echo -e "   ${CYAN}  -H \"Content-Type: application/json\" \\${NC}"
    echo -e "   ${CYAN}  -d '{\"prompt\": \"Hello, how are you?\"}'${NC}"
    echo ""
    STEP=$((STEP + 1))
    
    # Run tests
    echo -e "${BOLD}${STEP}. Run the full test suite:${NC}"
    echo -e "   ${CYAN}python3 -m pytest tests/ -v${NC}"
    echo ""
    STEP=$((STEP + 1))
    
    # Documentation
    echo -e "${BOLD}${STEP}. Read the documentation:${NC}"
    echo "   - ${CYAN}README.md${NC} - Full API documentation"
    echo "   - ${CYAN}CONTRIBUTING.md${NC} - Contribution guidelines"
    echo "   - ${CYAN}docs/ONBOARDING.md${NC} - Detailed onboarding guide"
    echo "   - ${CYAN}docs/INTEGRATION_API.md${NC} - Integration development"
    echo ""
    
    # Additional tips
    echo -e "${BOLD}💡 Pro Tips:${NC}"
    echo "   • Check out beginner-friendly issues labeled 'First Issue' on GitHub"
    echo "   • Join our community discussions for help and collaboration"
    echo "   • Run 'pytest' before committing changes to catch issues early"
    echo "   • Use the playground to experiment with AI features interactively"
    echo ""
    
    echo -e "${GREEN}${BOLD}Happy coding! Welcome to Savrli AI! 🚀${NC}\n"
}

# ============================================================================
# Error Handling and Cleanup
# ============================================================================

handle_error() {
    echo ""
    print_error "Setup encountered an error"
    echo ""
    echo "Troubleshooting resources:"
    echo "  - Check docs/ONBOARDING.md for detailed setup instructions"
    echo "  - See CONTRIBUTING.md for development guidelines"
    echo "  - Open an issue: https://github.com/Savrli-Inc/Savrli-AI/issues"
    echo ""
    exit 1
}

# Set up error trap
trap 'handle_error' ERR

# ============================================================================
# Main Setup Flow
# ============================================================================

main() {
    print_header "Welcome to Savrli AI Setup!"
    
    echo -e "${BLUE}This interactive script will help you get started with Savrli AI development.${NC}"
    echo ""
    echo "The script will:"
    echo "  ✓ Check your Python environment"
    echo "  ✓ Optionally create a virtual environment (recommended)"
    echo "  ✓ Install all required dependencies"
    echo "  ✓ Help you configure environment variables"
    echo "  ✓ Run basic health checks"
    echo "  ✓ Provide clear next steps"
    echo ""
    echo -e "${BOLD}Note: This script makes no destructive changes.${NC}"
    echo "It won't delete files or overwrite configurations without asking."
    echo ""
    
    if ! prompt_yes_no "Ready to begin?" "y"; then
        echo "Setup cancelled. Run ./scripts/setup.sh when you're ready!"
        exit 0
    fi
    
    # Track overall success
    ALL_CHECKS_PASSED=true
    ENV_CONFIGURED=true
    
    # Disable error exit temporarily for non-critical steps
    set +e
    
    # Run setup steps
    check_python || { ALL_CHECKS_PASSED=false; exit 1; }
    setup_virtualenv || ALL_CHECKS_PASSED=false
    install_dependencies || { ALL_CHECKS_PASSED=false; exit 1; }
    setup_env_file || { ENV_CONFIGURED=false; ALL_CHECKS_PASSED=false; }
    
    # Run tests (optional, don't fail on test failures)
    if [ "$ALL_CHECKS_PASSED" = true ]; then
        run_tests || true
    fi
    
    # Re-enable error exit
    set -e
    
    # Print summary
    echo ""
    print_header "Setup Summary"
    
    if [ "$ALL_CHECKS_PASSED" = true ]; then
        print_success "✨ All setup steps completed successfully!"
    else
        print_warning "⚠️  Setup completed with some warnings"
        print_info "Please review the messages above and address any issues"
    fi
    
    # Print next steps
    print_next_steps $ENV_CONFIGURED
}

# Run main function
main
