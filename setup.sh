#!/bin/bash
#
# Savrli AI Setup Script (Bash version)
#
# This script automates the onboarding process for new developers:
# - Validates Python environment
# - Installs dependencies
# - Guides environment variable setup
# - Runs health checks
# - Provides helpful next steps
#
# Usage: ./setup.sh
#

set -e  # Exit on error

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Helper functions
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

# Check Python version
check_python() {
    print_info "Step 1: Checking Python version..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        echo "Please install Python 3.8 or higher and try again"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        print_success "Python $PYTHON_VERSION detected (3.8+ required)"
        return 0
    else
        print_error "Python $PYTHON_VERSION detected, but 3.8+ is required"
        echo "Please upgrade Python and try again"
        exit 1
    fi
}

# Check pip installation
check_pip() {
    print_info "Step 2: Checking pip installation..."
    
    if ! python3 -m pip --version &> /dev/null; then
        print_error "pip is not installed"
        echo "Please install pip and try again"
        exit 1
    fi
    
    print_success "pip is installed"
}

# Install dependencies
install_dependencies() {
    print_info "Step 3: Installing dependencies..."
    
    if python3 -m pip install -r requirements.txt --quiet; then
        print_success "Dependencies installed successfully"
        return 0
    else
        print_error "Failed to install dependencies"
        return 1
    fi
}

# Check/create .env file
setup_env_file() {
    print_info "Step 4: Checking environment configuration..."
    
    if [ -f .env ]; then
        # Check if OPENAI_API_KEY is set
        if grep -q "OPENAI_API_KEY" .env && ! grep -q "your-api-key" .env; then
            print_success ".env file configured"
            return 0
        else
            print_warning "OPENAI_API_KEY not properly configured in .env"
            return 1
        fi
    else
        print_warning ".env file not found"
        create_env_template
        return 1
    fi
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
    
    print_success "Created .env file template"
    print_warning "⚠️  Please edit .env and add your OPENAI_API_KEY before running the server"
}

# Run basic tests
run_tests() {
    print_info "Step 5: Running basic tests..."
    
    # Set test API key if not configured
    export OPENAI_API_KEY="${OPENAI_API_KEY:-test-key-for-setup}"
    
    if python3 -m pytest tests/ -v --tb=short -x 2>&1 | tail -20; then
        print_success "All tests passed"
        return 0
    else
        print_warning "Some tests failed, but this might be due to missing API key"
        print_info "You can run tests later with: python3 -m pytest tests/ -v"
        return 1
    fi
}

# Print next steps
print_next_steps() {
    ENV_CONFIGURED=$1
    
    print_header "Next Steps"
    
    STEP=1
    
    if [ "$ENV_CONFIGURED" = false ]; then
        echo -e "${BOLD}1. Configure your environment variables:${NC}"
        echo "   - Edit the .env file"
        echo "   - Add your OpenAI API key from: https://platform.openai.com/api-keys"
        echo "   - Optional: Configure integration platform tokens"
        echo ""
        STEP=2
    fi
    
    echo -e "${BOLD}${STEP}. Start the development server:${NC}"
    echo -e "   ${CYAN}uvicorn api.index:app --reload${NC}"
    echo "   The API will be available at http://localhost:8000"
    echo ""
    
    STEP=$((STEP + 1))
    echo -e "${BOLD}${STEP}. Try the interactive playground:${NC}"
    echo -e "   Open ${CYAN}http://localhost:8000/playground${NC} in your browser"
    echo "   Perfect for testing AI features without writing code!"
    echo ""
    
    STEP=$((STEP + 1))
    echo -e "${BOLD}${STEP}. Test the API with curl:${NC}"
    echo -e "   ${CYAN}curl -X POST http://localhost:8000/ai/chat \\"
    echo -e "     -H \"Content-Type: application/json\" \\"
    echo -e "     -d '{\"prompt\": \"Hello, how are you?\"}'${NC}"
    echo ""
    
    STEP=$((STEP + 1))
    echo -e "${BOLD}${STEP}. Run tests:${NC}"
    echo -e "   ${CYAN}python3 -m pytest tests/ -v${NC}"
    echo ""
    
    STEP=$((STEP + 1))
    echo -e "${BOLD}${STEP}. Read the documentation:${NC}"
    echo "   - README.md - Full API documentation"
    echo "   - CONTRIBUTING.md - Contribution guidelines"
    echo "   - docs/ONBOARDING_GUIDE.md - Detailed onboarding guide"
    echo ""
    
    print_info "💡 Pro tip: Check out beginner-friendly 'First Issue' labels in GitHub Issues!"
}

# Main setup flow
main() {
    print_header "Welcome to Savrli AI Setup!"
    echo -e "${BLUE}This script will help you get started with Savrli AI development.${NC}\n"
    
    ALL_CHECKS_PASSED=true
    ENV_CONFIGURED=true
    
    # Run all checks
    check_python || ALL_CHECKS_PASSED=false
    check_pip || ALL_CHECKS_PASSED=false
    install_dependencies || ALL_CHECKS_PASSED=false
    setup_env_file || { ENV_CONFIGURED=false; ALL_CHECKS_PASSED=false; }
    
    # Run tests if all checks passed
    if [ "$ALL_CHECKS_PASSED" = true ]; then
        run_tests || true  # Don't fail on test errors
    fi
    
    # Final summary
    print_header "Setup Summary"
    
    if [ "$ALL_CHECKS_PASSED" = true ]; then
        print_success "✨ Setup completed successfully! ✨"
        print_success "All checks passed - you're ready to start developing!"
    else
        print_warning "⚠️  Setup completed with warnings"
        print_info "Please review the warnings above and complete the required steps"
    fi
    
    # Print next steps
    print_next_steps $ENV_CONFIGURED
    
    echo -e "\n${GREEN}${BOLD}Happy coding! 🚀${NC}\n"
}

# Run main function
main
