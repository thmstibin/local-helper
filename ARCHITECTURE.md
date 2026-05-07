# 🏗️ Local Helper - Architecture Documentation

This document explains the technical architecture and design decisions behind Local Helper.

## 🎯 Design Goals

1. **Autonomous Operation**: Minimal user intervention after initial request
2. **Safety First**: Prevent data loss and unauthorized access
3. **Extensibility**: Easy to add new capabilities
4. **Transparency**: Clear visibility into what the agent is doing
5. **Local Control**: Run entirely on user's machine with API calls

## 📐 System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│                         (CLI/Future Web)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Agent Orchestration Layer                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Task Planner │  │   Executor   │  │   Progress   │      │
│  │  (Claude)    │  │              │  │   Tracker    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Capability Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ File Ops     │  │ Doc Processor│  │ Task Executor│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Safety Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Sandboxing  │  │   Backups    │  │   History    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    File System (Workspace)                   │
└─────────────────────────────────────────────────────────────┘
```

## 🧩 Core Components

### 1. Agent (`src/agent.py`)

**Purpose**: Orchestrates task execution using Claude API

**Key Responsibilities**:
- Receive natural language requests
- Create execution plans via Claude
- Coordinate task execution
- Track progress and report status

**Design Pattern**: Orchestrator/Coordinator

**Key Methods**:
```python
async def execute_task(user_request: str) -> Task
async def _create_plan(user_request: str) -> AgentPlan
async def _execute_plan(task: Task, plan: AgentPlan) -> Dict
```

**Flow**:
1. User request → Claude API (planning)
2. Parse plan into structured actions
3. Execute actions sequentially
4. Report progress at each step
5. Return results

### 2. File Operations (`src/file_operations.py`)

**Purpose**: Safe file system operations with sandboxing

**Key Responsibilities**:
- Read/write/move/copy/delete files
- Enforce workspace boundaries
- Create backups before modifications
- Log all operations

**Design Pattern**: Facade with Safety Wrapper

**Security Features**:
- Path validation (prevent directory traversal)
- Workspace sandboxing
- File size limits
- Automatic backups

**Key Methods**:
```python
def read_file(file_path: Path) -> str
def write_file(file_path: Path, content: str) -> Path
def move_file(source: Path, destination: Path) -> Path
def _is_safe_path(path: Path) -> bool  # Security check
```

### 3. Task Executor (`src/task_executor.py`)

**Purpose**: Execute specific actions on files

**Key Responsibilities**:
- Translate high-level actions to file operations
- Handle different action types
- Coordinate with document processor
- Return structured results

**Design Pattern**: Command Pattern

**Supported Actions**:
- `read_file`: Read file contents
- `write_file`: Create/update files
- `organize_files`: Move files based on criteria
- `extract_data`: Extract from documents
- `generate_report`: Create reports
- `search_files`: Find files
- `batch_process`: Process multiple files

**Extensibility**: Easy to add new action handlers

### 4. Document Processor (`src/document_processor.py`)

**Purpose**: Extract data from various document formats

**Key Responsibilities**:
- Parse different file formats
- Extract structured data
- Handle format-specific operations

**Supported Formats**:
- Text files (.txt)
- JSON (.json)
- CSV (.csv)
- PDF (.pdf) - via PyPDF2
- Word (.docx) - via python-docx
- Excel (.xlsx) - via openpyxl

**Design Pattern**: Strategy Pattern (different extractors per format)

### 5. Configuration (`src/config.py`)

**Purpose**: Centralized configuration management

**Key Responsibilities**:
- Load environment variables
- Validate configuration
- Provide type-safe config access

**Design Pattern**: Singleton Configuration

**Uses**: Pydantic for validation and type safety

### 6. Models (`src/models.py`)

**Purpose**: Data structures and types

**Key Models**:
- `Task`: Represents a user task
- `TaskStatus`: Enum for task states
- `AgentAction`: Individual action in a plan
- `AgentPlan`: Complete execution plan
- `ProgressUpdate`: Progress notification

**Design Pattern**: Data Transfer Objects (DTOs)

### 7. CLI (`src/cli.py`)

**Purpose**: User interface

**Key Responsibilities**:
- Display welcome and help
- Accept user input
- Show progress updates
- Display results

**Uses**: Rich library for beautiful terminal output

## 🔄 Execution Flow

### Complete Task Execution

```
1. User Input
   │
   ├─→ "Organize my files by type"
   │
2. Agent.execute_task()
   │
   ├─→ Create Task object
   │   Status: PENDING
   │
3. Agent._create_plan()
   │
   ├─→ Build context (workspace info)
   ├─→ Call Claude API with system + user prompt
   ├─→ Parse JSON response
   ├─→ Create AgentPlan with actions
   │   Status: PLANNING → IN_PROGRESS
   │
4. Agent._execute_plan()
   │
   ├─→ For each action in plan:
   │   │
   │   ├─→ Send progress update
   │   ├─→ TaskExecutor.execute_action()
   │   │   │
   │   │   ├─→ Route to appropriate handler
   │   │   ├─→ FileOperations.* (with safety checks)
   │   │   └─→ Return result
   │   │
   │   └─→ Collect results
   │
5. Complete Task
   │
   ├─→ Status: COMPLETED
   ├─→ Store results
   └─→ Display to user
```

### Safety Checks Flow

```
User Action Request
   │
   ▼
TaskExecutor
   │
   ▼
FileOperations._is_safe_path()
   │
   ├─→ ✅ Path within workspace → Continue
   │
   └─→ ❌ Path outside workspace → Raise ValueError
   │
   ▼
FileOperations._create_backup()
   │
   ├─→ If file exists and backup enabled
   └─→ Copy to .backups/
   │
   ▼
Perform Operation
   │
   ▼
FileOperations._log_operation()
   │
   └─→ Record in operation history
```

## 🔐 Security Architecture

### Defense in Depth

1. **Workspace Sandboxing**
   - All paths validated against workspace root
   - Prevents directory traversal (../)
   - Rejects absolute paths outside workspace

2. **File Size Limits**
   - Configurable max file size
   - Prevents memory exhaustion
   - Default: 50MB

3. **Backup System**
   - Automatic backups before modifications
   - Timestamped backup files
   - Stored in separate .backups/ directory

4. **Operation Logging**
   - All file operations logged
   - Includes timestamp, operation type, paths
   - Enables audit trail

5. **API Key Protection**
   - Stored in .env (not committed)
   - Loaded via environment variables
   - Never logged or displayed

## 🎨 Design Patterns Used

### 1. Orchestrator Pattern
**Where**: `LocalHelperAgent`
**Why**: Coordinates multiple subsystems without tight coupling

### 2. Facade Pattern
**Where**: `FileOperations`
**Why**: Simplifies file system operations with safety layer

### 3. Command Pattern
**Where**: `TaskExecutor` action handlers
**Why**: Encapsulates operations as objects, easy to extend

### 4. Strategy Pattern
**Where**: `DocumentProcessor` format handlers
**Why**: Different algorithms for different file types

### 5. Observer Pattern
**Where**: Progress callbacks
**Why**: Decouple progress reporting from execution

## 🔌 Extension Points

### Adding New Action Types

1. Add action type to `TaskExecutor`
2. Implement handler method
3. Claude will automatically use it in plans

```python
async def _handle_new_action(self, action: AgentAction) -> Dict[str, Any]:
    # Implementation
    return {"success": True}
```

### Adding New Document Formats

1. Add format handler to `DocumentProcessor`
2. Register in `extract_data()` handlers dict

```python
async def _extract_new_format(self, file_path: Path) -> Dict[str, Any]:
    # Implementation
    return {"type": "new_format", "data": ...}
```

### Adding New Interfaces

Current: CLI
Future: Web UI, API, Desktop App

Interface requirements:
- Call `agent.execute_task()`
- Handle progress callbacks
- Display results

## 📊 Data Flow

### Configuration Flow
```
.env file → load_dotenv() → Config (Pydantic) → Components
```

### Task Data Flow
```
User Input → Task → AgentPlan → Actions → Results → Task
```

### File Data Flow
```
Workspace → FileOperations → TaskExecutor → Agent → User
```

## 🧪 Testing Strategy

### Unit Tests (Future)
- Test individual components
- Mock external dependencies (Claude API, file system)
- Test safety checks

### Integration Tests (Future)
- Test complete workflows
- Use temporary workspace
- Verify file operations

### Manual Testing
- Use `test_setup.py` for installation verification
- Test with sample workspace

## 🚀 Performance Considerations

### API Calls
- One planning call per task
- No calls during execution (unless extended)
- Typical: 500-2000 tokens per task

### Memory Usage
- Files loaded into memory for processing
- Size limits prevent exhaustion
- Streaming for large files (future enhancement)

### Concurrency
- Currently sequential execution
- Future: Parallel action execution where safe

## 📈 Future Enhancements

### Planned Features
1. **Web Interface**: Browser-based UI
2. **Undo System**: Reverse operations using history
3. **Scheduled Tasks**: Cron-like automation
4. **Plugins**: User-defined actions
5. **Multi-workspace**: Manage multiple workspaces
6. **Collaboration**: Share workflows
7. **Advanced Search**: Semantic file search
8. **Version Control**: Track file changes

### Architecture Evolution
- Event-driven architecture for real-time updates
- Plugin system for extensibility
- Database for operation history
- Caching layer for performance

## 📚 Dependencies Rationale

| Package | Purpose | Why Chosen |
|---------|---------|------------|
| anthropic | Claude API | Official SDK, well-maintained |
| rich | Terminal UI | Beautiful output, progress bars |
| pydantic | Validation | Type safety, data validation |
| python-dotenv | Config | Standard for .env files |
| PyPDF2 | PDF processing | Pure Python, no dependencies |
| openpyxl | Excel | Read/write .xlsx files |
| python-docx | Word docs | Read/write .docx files |

## 🎓 Learning Resources

To understand the codebase:
1. Start with `main.py` → `cli.py`
2. Follow a task through `agent.py`
3. Explore `file_operations.py` for safety
4. Check `models.py` for data structures

Key concepts:
- Async/await for task execution
- Pydantic for data validation
- Path manipulation for safety
- JSON parsing for Claude responses
