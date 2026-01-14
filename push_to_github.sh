#!/bin/bash

# Local Helper - GitHub Push Script
# This script will push your code to GitHub and create a release

set -e  # Exit on error

echo "🚀 Local Helper - GitHub Push Script"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Final security check
echo -e "${BLUE}Step 1: Running final security check...${NC}"
echo ""

# Check for actual API keys
if grep -r "sk-ant-api[0-9]" . --include="*.py" --include="*.env" 2>/dev/null | grep -v "xxxxx"; then
    echo -e "${RED}❌ ERROR: Found actual API key in code!${NC}"
    echo "Please remove it before pushing."
    exit 1
fi

# Check if .env exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  WARNING: .env file exists${NC}"
    echo "Make sure it's in .gitignore (it should be)"
    grep "^\.env$" .gitignore > /dev/null || {
        echo -e "${RED}❌ ERROR: .env is not in .gitignore!${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ .env is properly ignored${NC}"
fi

echo -e "${GREEN}✅ Security check passed - no secrets found${NC}"
echo ""

# Step 2: Check git status
echo -e "${BLUE}Step 2: Checking git status...${NC}"
echo ""

# Add new files
git add .

# Show what will be committed
echo "Files to be committed:"
git status --short
echo ""

# Count files
FILE_COUNT=$(git ls-files --cached | wc -l | tr -d ' ')
echo -e "${GREEN}✅ Total files staged: $FILE_COUNT${NC}"
echo ""

# Step 3: Commit
echo -e "${BLUE}Step 3: Creating commit...${NC}"
echo ""

# Use the prepared commit message
if [ -f "COMMIT_MESSAGE.txt" ]; then
    git commit -F COMMIT_MESSAGE.txt
    echo -e "${GREEN}✅ Commit created with detailed message${NC}"
else
    git commit -m "🎉 Initial Release: Local Helper v0.1.0

Open-source, cross-platform alternative to Claude Cowork

Features:
- Autonomous task execution with Claude API
- Cross-platform file management
- Document processing (PDF, Excel, Word, CSV, JSON)
- Safe operations with sandboxing and backups
- Beautiful CLI interface
- Comprehensive documentation

Ready for production use!"
    echo -e "${GREEN}✅ Commit created${NC}"
fi
echo ""

# Step 4: Set up remote
echo -e "${BLUE}Step 4: Setting up GitHub remote...${NC}"
echo ""

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "Remote 'origin' already exists:"
    git remote -v
    echo ""
    echo -e "${YELLOW}Updating remote URL...${NC}"
    git remote set-url origin https://github.com/thmstibin/local-helper.git
else
    echo "Adding remote 'origin'..."
    git remote add origin https://github.com/thmstibin/local-helper.git
fi

echo -e "${GREEN}✅ Remote configured${NC}"
echo ""

# Step 5: Push to GitHub
echo -e "${BLUE}Step 5: Pushing to GitHub...${NC}"
echo ""
echo "This will push to: https://github.com/thmstibin/local-helper"
echo ""
echo -e "${YELLOW}Press Enter to continue, or Ctrl+C to cancel...${NC}"
read

# Push to main branch
git push -u origin main

echo ""
echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
echo ""

# Step 6: Instructions for creating release
echo -e "${BLUE}Step 6: Next steps - Create a release${NC}"
echo ""
echo "To create a release on GitHub:"
echo ""
echo "1. Go to: https://github.com/thmstibin/local-helper/releases/new"
echo ""
echo "2. Fill in the release form:"
echo "   - Tag: v0.1.0"
echo "   - Title: Local Helper v0.1.0 - Initial Release"
echo "   - Description: Copy from RELEASE_NOTES_v0.1.0.md"
echo ""
echo "3. Click 'Publish release'"
echo ""
echo -e "${GREEN}🎉 All done! Your code is now on GitHub!${NC}"
echo ""
echo "Repository: https://github.com/thmstibin/local-helper"
echo ""
echo "Don't forget to:"
echo "  - Add repository description on GitHub"
echo "  - Add topics/tags: ai-agent, claude-api, automation, python, file-management"
echo "  - Create the v0.1.0 release"
echo "  - Share your project!"
echo ""

