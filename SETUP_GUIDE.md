# 🚀 Local Helper - Complete Setup Guide

This guide will walk you through setting up Local Helper on your machine.

## 📋 Prerequisites

### Required
- **Python 3.9 or higher**
  - Check version: `python --version` or `python3 --version`
  - Download from: https://www.python.org/downloads/

- **Anthropic API Key**
  - Sign up at: https://console.anthropic.com/
  - Navigate to API Keys section
  - Create a new API key
  - **Important**: Keep this key secure!

### Optional
- **Git** (for cloning the repository)
- **Virtual environment** (recommended for isolation)

## 🔧 Installation Steps

### Step 1: Get the Code

**Option A: Clone with Git**
```bash
git clone <repository-url>
cd "Local Helper"
```

**Option B: Download ZIP**
1. Download the project as ZIP
2. Extract to your desired location
3. Open terminal/command prompt in that folder

### Step 2: Create Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `anthropic` - Claude API client
- `rich` - Beautiful terminal output
- `pydantic` - Data validation
- `python-dotenv` - Environment configuration
- `PyPDF2` - PDF processing
- `openpyxl` - Excel processing
- `python-docx` - Word document processing
- And other utilities

### Step 4: Configure Environment

1. **Copy the example configuration:**
```bash
cp .env.example .env
```

2. **Edit `.env` file:**
```bash
# On macOS/Linux
nano .env

# On Windows
notepad .env
```

3. **Add your configuration:**
```env
# Required: Your Anthropic API key
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx

# Required: Path to your workspace folder
WORKSPACE_PATH=/Users/yourname/Documents/workspace

# Optional: Advanced settings
MODEL_NAME=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
TEMPERATURE=0.7
MAX_FILE_SIZE_MB=50
ENABLE_UNDO=true
BACKUP_ENABLED=true
BACKUP_PATH=./.backups
LOG_LEVEL=INFO
```

### Step 5: Create Workspace Folder

Create the folder where Local Helper will work:

```bash
mkdir -p ~/Documents/local-helper-workspace
```

Update `WORKSPACE_PATH` in `.env` to point to this folder.

### Step 6: Test Installation

Run Local Helper:

```bash
python main.py
```

You should see the welcome screen! 🎉

## 🔍 Verification Checklist

- [ ] Python 3.9+ installed
- [ ] All dependencies installed without errors
- [ ] `.env` file created with API key
- [ ] Workspace folder exists
- [ ] Program starts without errors
- [ ] Can see welcome screen

## 🎯 First Run

### Test with a Simple Command

1. Start Local Helper: `python main.py`
2. Try a simple command: `List all files in the workspace`
3. The agent should respond with a list of files (or empty if workspace is empty)

### Add Test Files

Create some test files in your workspace:

```bash
cd ~/Documents/local-helper-workspace
echo "Test content" > test1.txt
echo "More content" > test2.txt
mkdir documents
echo "Document content" > documents/doc1.txt
```

Now try: `Organize files by type`

## ⚙️ Configuration Options Explained

### API Configuration

```env
ANTHROPIC_API_KEY=your_key_here
```
Your API key from Anthropic. **Required**.

```env
MODEL_NAME=claude-3-5-sonnet-20241022
```
Which Claude model to use. Options:
- `claude-3-5-sonnet-20241022` (recommended, balanced)
- `claude-3-opus-20240229` (most capable, slower)
- `claude-3-haiku-20240307` (fastest, less capable)

```env
MAX_TOKENS=4096
```
Maximum tokens for Claude responses. Higher = more detailed plans.

```env
TEMPERATURE=0.7
```
Creativity level (0.0-1.0). Lower = more focused, Higher = more creative.

### Workspace Configuration

```env
WORKSPACE_PATH=/path/to/workspace
```
**Required**. The folder where Local Helper can work. Must be absolute path.

```env
MAX_FILE_SIZE_MB=50
```
Maximum file size to process. Prevents memory issues with huge files.

### Safety Configuration

```env
ENABLE_UNDO=true
```
Enable operation history tracking for potential undo.

```env
BACKUP_ENABLED=true
```
Automatically backup files before modification.

```env
BACKUP_PATH=./.backups
```
Where to store backups. Can be absolute or relative path.

### Logging

```env
LOG_LEVEL=INFO
```
Logging verbosity. Options: DEBUG, INFO, WARNING, ERROR

```env
LOG_FILE=./local_helper.log
```
Where to save logs.

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'anthropic'"

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### "API key not found"

**Solution:** Check your `.env` file
1. Ensure `.env` exists in project root
2. Verify `ANTHROPIC_API_KEY` is set
3. No quotes needed around the key
4. No spaces around the `=`

### "Workspace path does not exist"

**Solution:** Create the workspace folder
```bash
mkdir -p /path/to/your/workspace
```

Or update `WORKSPACE_PATH` in `.env` to an existing folder.

### "Permission denied" errors

**Solution:** Check folder permissions
```bash
# On macOS/Linux
chmod 755 /path/to/workspace

# Or choose a folder you own
WORKSPACE_PATH=~/Documents/local-helper-workspace
```

### "Rate limit exceeded"

**Solution:** You've hit API rate limits
- Wait a few minutes
- Reduce request frequency
- Check your Anthropic account limits

### Program crashes immediately

**Solution:** Check logs
```bash
cat local_helper.log
```

Look for error messages and stack traces.

## 🔐 Security Best Practices

### Protect Your API Key

1. **Never commit `.env` to version control**
   - `.env` is in `.gitignore` by default

2. **Use environment variables in production**
   ```bash
   export ANTHROPIC_API_KEY=your_key
   python main.py
   ```

3. **Rotate keys regularly**
   - Generate new keys periodically
   - Revoke old keys

### Workspace Security

1. **Use a dedicated workspace folder**
   - Don't point to system folders
   - Don't use your entire home directory

2. **Review operations before confirming**
   - Check what the agent plans to do
   - Understand the impact

3. **Keep backups enabled**
   - Provides safety net for mistakes

## 📊 Resource Usage

### API Costs

Local Helper uses the Anthropic API, which charges per token:
- Planning: ~500-2000 tokens per task
- Execution: Varies by complexity
- Typical task: $0.01-0.05

Monitor usage at: https://console.anthropic.com/

### Disk Space

- Backups can accumulate over time
- Clean old backups periodically:
  ```bash
  rm -rf .backups/*
  ```

### Memory

- Processes files in memory
- Large files (>50MB) are rejected by default
- Adjust `MAX_FILE_SIZE_MB` if needed

## 🚀 Next Steps

1. ✅ Complete installation
2. 📖 Read [EXAMPLES.md](EXAMPLES.md) for usage examples
3. 🎯 Try simple tasks first
4. 📚 Explore advanced workflows
5. 🛠️ Customize configuration for your needs

## 💬 Getting Help

If you encounter issues:

1. Check this guide
2. Review logs: `cat local_helper.log`
3. Check [EXAMPLES.md](EXAMPLES.md) for usage patterns
4. Verify your configuration in `.env`

## 🎓 Learning Path

**Week 1: Basics**
- File listing and searching
- Simple organization tasks
- Reading file contents

**Week 2: Intermediate**
- Document processing
- Batch operations
- Report generation

**Week 3: Advanced**
- Complex workflows
- Custom automation
- Multi-step tasks

Happy automating! 🚀
