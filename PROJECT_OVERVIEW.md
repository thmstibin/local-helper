# 📋 Local Helper - Project Overview

## 🎯 What is Local Helper?

Local Helper is an **open-source, autonomous AI assistant** that replicates the functionality of Anthropic's Claude Cowork, but runs locally on any platform without requiring the Claude Desktop app.

It uses the Claude API to understand natural language requests and autonomously execute file management and productivity tasks on your local machine.

## 🌟 Key Features

### ✅ Implemented Features

1. **🤖 Autonomous Task Execution**
   - Natural language understanding
   - Automatic task planning via Claude API
   - Multi-step workflow execution
   - Real-time progress tracking

2. **📁 File Management**
   - Read, write, create, delete files
   - Move, copy, rename operations
   - Organize files by type, date, or custom criteria
   - Smart file search (by name or content)

3. **📄 Document Processing**
   - PDF text extraction (PyPDF2)
   - Excel data extraction (openpyxl)
   - Word document processing (python-docx)
   - CSV and JSON parsing
   - Generic text file handling

4. **📊 Report Generation**
   - Create summaries from multiple files
   - Generate file inventories
   - Extract and combine data
   - Custom report formats

5. **⚡ Batch Operations**
   - Process multiple files at once
   - Batch rename with patterns
   - Bulk organization
   - Parallel processing ready

6. **🔒 Safety & Security**
   - Workspace sandboxing (prevents directory traversal)
   - Automatic file backups before modifications
   - Operation history logging
   - File size limits
   - Path validation

7. **🎨 User Interface**
   - Rich CLI with beautiful formatting
   - Progress bars and status updates
   - Interactive prompts
   - Helpful error messages

## 📁 Project Structure

```
Local Helper/
│
├── 📄 Core Application Files
│   ├── main.py                    # Entry point
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example              # Configuration template
│   └── .gitignore                # Git ignore rules
│
├── 📦 Source Code (src/)
│   ├── __init__.py               # Package initialization
│   ├── agent.py                  # Core autonomous agent
│   ├── config.py                 # Configuration management
│   ├── models.py                 # Data models and types
│   ├── file_operations.py        # Safe file operations
│   ├── task_executor.py          # Task execution engine
│   ├── document_processor.py     # Document format handlers
│   └── cli.py                    # Command-line interface
│
├── 📚 Documentation
│   ├── README.md                 # Main documentation
│   ├── SETUP_GUIDE.md           # Installation instructions
│   ├── EXAMPLES.md              # Usage examples
│   ├── ARCHITECTURE.md          # Technical architecture
│   ├── COMPARISON.md            # vs Claude Cowork
│   └── PROJECT_OVERVIEW.md      # This file
│
└── 🛠️ Utilities
    ├── test_setup.py            # Installation verification
    ├── quickstart.sh            # Quick setup script
    └── LICENSE                  # MIT License
```

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────┐
│         User (Natural Language)          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│          CLI Interface (Rich)            │
│  • Input handling                        │
│  • Progress display                      │
│  • Result formatting                     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      LocalHelperAgent (Orchestrator)     │
│  • Task planning (Claude API)            │
│  • Execution coordination                │
│  • Progress tracking                     │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌─────────────┐  ┌─────────────────┐
│ Task        │  │ Document         │
│ Executor    │  │ Processor        │
│             │  │                  │
│ • Actions   │  │ • PDF            │
│ • Workflows │  │ • Excel          │
│ • Batch ops │  │ • Word           │
└──────┬──────┘  └────────┬─────────┘
       │                  │
       └────────┬─────────┘
                ▼
┌─────────────────────────────────────────┐
│      FileOperations (Safety Layer)       │
│  • Sandboxing                            │
│  • Backups                               │
│  • Validation                            │
│  • Logging                               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Workspace (File System)             │
└─────────────────────────────────────────┘
```

## 🔄 How It Works

### Execution Flow

1. **User Input**: Natural language request (e.g., "Organize my files by type")

2. **Planning Phase**:
   - Agent gathers workspace context
   - Sends request to Claude API with system prompt
   - Claude returns structured JSON plan with actions

3. **Execution Phase**:
   - Agent executes each action sequentially
   - TaskExecutor routes to appropriate handler
   - FileOperations performs safe file operations
   - Progress updates sent to UI

4. **Completion**:
   - Results collected and formatted
   - Summary displayed to user
   - Operation logged for history

### Example Task Flow

```
User: "Create a summary of all text files"
  ↓
Agent: Plans with Claude
  ↓
Plan: [
  1. Find all .txt files
  2. Read each file
  3. Extract key information
  4. Generate summary report
  5. Save as summary.txt
]
  ↓
Execute: Each step with progress updates
  ↓
Result: summary.txt created, stats displayed
```

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.9+**: Main programming language
- **Anthropic API**: Claude for task planning
- **asyncio**: Asynchronous task execution

### Key Libraries
- **anthropic**: Official Claude API client
- **rich**: Beautiful terminal UI
- **pydantic**: Data validation and settings
- **python-dotenv**: Environment configuration

### Document Processing
- **PyPDF2**: PDF text extraction
- **openpyxl**: Excel file handling
- **python-docx**: Word document processing

## 🎯 Use Cases

### Personal Productivity
- Organize downloads folder
- Clean up desktop
- Find and archive old files
- Create file inventories

### Document Management
- Extract data from invoices
- Summarize reports
- Combine multiple documents
- Convert file formats

### Data Processing
- Extract data from spreadsheets
- Parse CSV files
- Generate reports from data
- Analyze document collections

### Automation
- Scheduled file organization
- Batch file processing
- Automated backups
- Workflow automation

## 🆚 vs Claude Cowork

| Aspect | Claude Cowork | Local Helper |
|--------|---------------|--------------|
| Platform | macOS only | Cross-platform |
| Deployment | Desktop app | Python app |
| Cost | $20/month (Max) | Pay-per-use API |
| Open Source | No | Yes |
| Customizable | No | Yes |
| Extensible | No | Yes |

**See [COMPARISON.md](COMPARISON.md) for detailed comparison**

## 🚀 Getting Started

### Quick Start (3 steps)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure**:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

3. **Run**:
   ```bash
   python main.py
   ```

**See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions**

## 📖 Documentation Guide

- **New users**: Start with [README.md](README.md) and [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Usage examples**: See [EXAMPLES.md](EXAMPLES.md)
- **Technical details**: Read [ARCHITECTURE.md](ARCHITECTURE.md)
- **Comparison**: Check [COMPARISON.md](COMPARISON.md)

## 🔮 Future Roadmap

### Phase 1: Core Enhancements (Current)
- ✅ Basic file operations
- ✅ Document processing
- ✅ CLI interface
- ✅ Safety features

### Phase 2: Advanced Features (Next)
- 🔄 Web interface
- 🔄 Enhanced undo system
- 🔄 Plugin architecture
- 🔄 Scheduled tasks

### Phase 3: Scaling (Future)
- 📋 Multi-workspace support
- 📋 Collaboration features
- 📋 Cloud integration
- 📋 Mobile app

## 🤝 Contributing

This is an open-source project. Contributions welcome!

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Areas for Contribution
- New document format processors
- Additional action types
- UI improvements
- Documentation
- Bug fixes
- Performance optimizations

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- **Anthropic**: For Claude API and inspiration from Cowork
- **Open Source Community**: For the excellent libraries used

## 📞 Support

- **Documentation**: Check the docs/ folder
- **Issues**: Report bugs and request features
- **Discussions**: Share ideas and ask questions

## 🎓 Learning Resources

### For Users
1. [SETUP_GUIDE.md](SETUP_GUIDE.md) - Installation
2. [EXAMPLES.md](EXAMPLES.md) - Usage examples
3. [README.md](README.md) - Overview

### For Developers
1. [ARCHITECTURE.md](ARCHITECTURE.md) - System design
2. Source code comments
3. [COMPARISON.md](COMPARISON.md) - Design decisions

## 📊 Project Status

**Current Version**: 0.1.0 (Initial Release)

**Status**: ✅ Functional, 🔄 Active Development

**Stability**: Beta - Ready for testing and feedback

## 🎯 Project Goals

1. **Accessibility**: Make AI-powered file management available to everyone
2. **Transparency**: Open-source, understandable code
3. **Flexibility**: Cross-platform, customizable, extensible
4. **Safety**: Protect user data with robust safety features
5. **Education**: Help people learn about AI agents

## 💡 Philosophy

Local Helper is built on these principles:

- **User Control**: You own your data and control the agent
- **Transparency**: Open source, clear operations
- **Safety First**: Multiple layers of protection
- **Simplicity**: Easy to use, easy to understand
- **Extensibility**: Build on top, customize freely

---

**Ready to get started?** → [SETUP_GUIDE.md](SETUP_GUIDE.md)

**Want to see examples?** → [EXAMPLES.md](EXAMPLES.md)

**Curious about the tech?** → [ARCHITECTURE.md](ARCHITECTURE.md)
