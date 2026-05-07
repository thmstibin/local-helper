# 🤖 Local Helper

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**An open-source, cross-platform alternative to Claude Cowork**

A local, autonomous AI assistant inspired by Claude Cowork that helps with file management and productivity tasks. Unlike Claude Desktop, this runs entirely on your local machine using the Claude API directly.

## 🌟 Features

- **🤖 Autonomous Task Execution**: Give natural language instructions and let the AI handle the rest
- **📁 File Management**: Organize, search, move, copy, and manage files automatically
- **📄 Document Processing**: Extract data from PDFs, Excel, Word, and other document formats
- **📊 Report Generation**: Create summaries and reports from multiple files
- **🔍 Smart Search**: Find files by name, content, or metadata
- **⚡ Batch Operations**: Process multiple files at once
- **🔒 Safety First**: Automatic backups, sandboxed workspace, and operation history
- **📈 Progress Tracking**: Real-time updates on task execution

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface (CLI)                  │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│              Autonomous Agent (Claude API)               │
│  • Task Planning    • Execution    • Progress Tracking  │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌───▼────────┐ ┌─▼──────────────┐
│ File Ops     │ │ Doc Proc   │ │ Task Executor  │
│ • Read/Write │ │ • PDF      │ │ • Organize     │
│ • Move/Copy  │ │ • Excel    │ │ • Search       │
│ • Delete     │ │ • Word     │ │ • Batch Ops    │
│ • Backup     │ │ • CSV/JSON │ │ • Reports      │
└──────────────┘ └────────────┘ └────────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
        ┌─────────────▼─────────────┐
        │   Sandboxed Workspace     │
        │   (User-defined folder)   │
        └───────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone or download this repository**

```bash
cd "Local Helper"
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure your environment**

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
ANTHROPIC_API_KEY=your_api_key_here
WORKSPACE_PATH=/path/to/your/workspace
```

4. **Run Local Helper**

```bash
python main.py
```

## 📖 Usage

### Interactive Mode

Simply run the program and type your requests in natural language:

```
What would you like me to do? Organize my downloads folder by file type
```

### Example Commands

**File Organization:**
```
- "Organize all files by type"
- "Move all PDFs to a Documents folder"
- "Rename all images with today's date"
```

**Document Processing:**
```
- "Extract data from expenses.xlsx"
- "Summarize all text files in the reports folder"
- "Create a list of all PDF files"
```

**Search & Analysis:**
```
- "Find all files containing 'budget'"
- "List files modified in the last week"
- "Show me all Excel files larger than 1MB"
```

**Report Generation:**
```
- "Create a summary report of all CSV files"
- "Generate an inventory of all documents"
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Required |
| `WORKSPACE_PATH` | Path to workspace folder | `./workspace` |
| `MODEL_NAME` | Claude model to use | `claude-3-5-sonnet-20241022` |
| `MAX_FILE_SIZE_MB` | Maximum file size to process | `50` |
| `ENABLE_UNDO` | Enable undo functionality | `true` |
| `BACKUP_ENABLED` | Auto-backup before changes | `true` |
| `BACKUP_PATH` | Backup storage location | `./.backups` |

## 🛡️ Safety Features

### Sandboxing
All file operations are restricted to the configured workspace directory. The system prevents directory traversal attacks.

### Automatic Backups
Before modifying or deleting files, Local Helper creates backups in the `.backups` folder.

### Operation History
All file operations are logged with timestamps and can be reviewed.

### File Size Limits
Large files are rejected to prevent memory issues.

## 🏛️ Project Structure

```
Local Helper/
├── src/
│   ├── __init__.py
│   ├── agent.py              # Core autonomous agent
│   ├── config.py             # Configuration management
│   ├── models.py             # Data models
│   ├── file_operations.py    # Safe file operations
│   ├── task_executor.py      # Task execution engine
│   ├── document_processor.py # Document processing
│   └── cli.py                # Command-line interface
├── main.py                   # Entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Example configuration
└── README.md                # This file
```

## 🆚 Comparison with Claude Cowork

| Feature | Claude Cowork | Local Helper |
|---------|---------------|--------------|
| **Platform** | macOS only (Desktop app) | Cross-platform (Python) |
| **Deployment** | Requires Claude Desktop | Standalone application |
| **API** | Built-in | Uses Anthropic API |
| **Customization** | Limited | Fully customizable |
| **Open Source** | No | Yes |
| **Cost** | Claude Max subscription | Pay-per-use API |
| **Workspace** | Single folder | Configurable |
| **Extensibility** | Closed | Open for extensions |

## 🔌 How It Works

1. **User Input**: You provide a natural language request
2. **Planning**: The agent uses Claude to create a detailed execution plan
3. **Execution**: Each action in the plan is executed step-by-step
4. **Progress Updates**: Real-time feedback on what's happening
5. **Results**: Summary of completed actions and affected files

### Example Flow

```
User: "Organize my files by type"
  ↓
Agent: Creates plan with Claude API
  ↓
Plan: [
  1. List all files in workspace
  2. Group files by extension
  3. Create folders for each type
  4. Move files to respective folders
]
  ↓
Executor: Executes each step
  ↓
Result: Files organized, summary displayed
```
