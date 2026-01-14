#!/bin/bash

# Fix GitHub Authentication and Push
# This script helps resolve the 403 permission error

set -e

echo "🔧 GitHub Authentication Fix"
echo "============================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}The error shows: 'Permission denied to thmstib'${NC}"
echo -e "${BLUE}But the repo is: 'thmstibin/local-helper'${NC}"
echo ""
echo "This is a GitHub authentication issue. Let's fix it!"
echo ""

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    echo -e "${GREEN}✅ GitHub CLI (gh) is installed${NC}"
    echo ""
    echo "Option 1: Authenticate with GitHub CLI (Recommended)"
    echo "=================================================="
    echo ""
    echo "Run these commands:"
    echo ""
    echo -e "${YELLOW}gh auth login${NC}"
    echo ""
    echo "Then select:"
    echo "  - GitHub.com"
    echo "  - HTTPS"
    echo "  - Login with a web browser"
    echo ""
    echo "After authentication, run:"
    echo -e "${YELLOW}git push -u origin main${NC}"
    echo ""
else
    echo -e "${YELLOW}⚠️  GitHub CLI (gh) is not installed${NC}"
    echo ""
    echo "Option 1: Install GitHub CLI (Recommended)"
    echo "=========================================="
    echo ""
    echo "Install with Homebrew:"
    echo -e "${YELLOW}brew install gh${NC}"
    echo ""
    echo "Then authenticate:"
    echo -e "${YELLOW}gh auth login${NC}"
    echo ""
fi

echo ""
echo "Option 2: Use Personal Access Token"
echo "===================================="
echo ""
echo "1. Go to: https://github.com/settings/tokens/new"
echo ""
echo "2. Create a token with these settings:"
echo "   - Note: 'Local Helper Push'"
echo "   - Expiration: 90 days (or your preference)"
echo "   - Scopes: Check 'repo' (all repo permissions)"
echo ""
echo "3. Click 'Generate token' and COPY the token"
echo ""
echo "4. Update the remote URL with your token:"
echo ""
echo -e "${YELLOW}git remote set-url origin https://YOUR_TOKEN@github.com/thmstibin/local-helper.git${NC}"
echo ""
echo "   Replace YOUR_TOKEN with the token you copied"
echo ""
echo "5. Push:"
echo -e "${YELLOW}git push -u origin main${NC}"
echo ""

echo ""
echo "Option 3: Use SSH (Most Secure)"
echo "================================"
echo ""
echo "1. Generate SSH key (if you don't have one):"
echo -e "${YELLOW}ssh-keygen -t ed25519 -C \"your_email@example.com\"${NC}"
echo ""
echo "2. Add SSH key to ssh-agent:"
echo -e "${YELLOW}eval \"\$(ssh-agent -s)\"${NC}"
echo -e "${YELLOW}ssh-add ~/.ssh/id_ed25519${NC}"
echo ""
echo "3. Copy your public key:"
echo -e "${YELLOW}cat ~/.ssh/id_ed25519.pub | pbcopy${NC}"
echo ""
echo "4. Add to GitHub:"
echo "   - Go to: https://github.com/settings/ssh/new"
echo "   - Paste your key"
echo "   - Click 'Add SSH key'"
echo ""
echo "5. Change remote to SSH:"
echo -e "${YELLOW}git remote set-url origin git@github.com:thmstibin/local-helper.git${NC}"
echo ""
echo "6. Push:"
echo -e "${YELLOW}git push -u origin main${NC}"
echo ""

echo ""
echo "Option 4: Use GitHub Desktop (Easiest)"
echo "======================================="
echo ""
echo "1. Open GitHub Desktop"
echo "2. File → Add Local Repository"
echo "3. Choose this folder: $(pwd)"
echo "4. Click 'Publish repository'"
echo "5. Make sure 'thmstibin' is selected as the owner"
echo "6. Click 'Publish Repository'"
echo ""

echo ""
echo -e "${BLUE}Current Status:${NC}"
echo "  Repository: https://github.com/thmstibin/local-helper"
echo "  Branch: main"
echo "  Commit: Ready to push"
echo "  Files: $(git ls-files | wc -l | tr -d ' ') files staged"
echo ""

echo -e "${GREEN}Choose the option that works best for you!${NC}"
echo ""
echo "After authentication, you can push with:"
echo -e "${YELLOW}git push -u origin main${NC}"
echo ""

