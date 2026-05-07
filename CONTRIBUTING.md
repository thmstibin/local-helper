# Contributing to Local Helper

Thank you for your interest in contributing to Local Helper! 🎉

## 🌟 Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit code improvements
- 🧪 Add tests
- 🎨 Enhance the UI/UX

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/local-helper.git
cd local-helper
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

### Example:

```python
def process_file(file_path: Path) -> Dict[str, Any]:
    """Process a file and extract data.

    Args:
        file_path: Path to the file to process

    Returns:
        Dictionary containing extracted data

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    # Implementation
    pass
```

### Project Structure

```
src/
├── agent.py              # Core agent logic
├── file_operations.py    # File system operations
├── task_executor.py      # Task execution
├── document_processor.py # Document handling
├── cli.py               # User interface
├── config.py            # Configuration
└── models.py            # Data models
```

## 🧪 Testing

### Run Setup Test

```bash
python test_setup.py
```

### Manual Testing

```bash
# Create test workspace
mkdir -p test_workspace
echo "Test content" > test_workspace/test.txt

# Update .env
WORKSPACE_PATH=./test_workspace

# Run the application
python main.py
```

### Test Your Changes

Before submitting, test:
- ✅ Basic file operations work
- ✅ No errors in logs
- ✅ Documentation is updated
- ✅ Code follows style guidelines

## 📋 Commit Guidelines

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples:

```bash
git commit -m "feat: add support for markdown file processing"

git commit -m "fix: resolve path traversal vulnerability in file operations"

git commit -m "docs: update installation instructions for Windows"
```

## 🔄 Pull Request Process

### 1. Update Your Fork

```bash
git fetch upstream
git rebase upstream/main
```

### 2. Push Your Changes

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

- Go to GitHub and create a PR
- Fill out the PR template
- Link any related issues
- Wait for review

### PR Checklist:

- [ ] Code follows project style guidelines
- [ ] Documentation updated (if needed)
- [ ] Tested manually
- [ ] No new warnings or errors
- [ ] Commit messages are clear

## 🐛 Reporting Bugs

### Before Reporting:

1. Check existing issues
2. Try the latest version
3. Verify it's reproducible

### Bug Report Template:

```markdown
**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., macOS 14.0]
- Python version: [e.g., 3.11.0]
- Local Helper version: [e.g., 0.1.0]

**Logs:**
```
Paste relevant logs here
```
```

## 💡 Suggesting Features

### Feature Request Template:

```markdown
**Feature Description:**
Clear description of the feature

**Use Case:**
Why is this feature needed?

**Proposed Solution:**
How should it work?

**Alternatives Considered:**
Other approaches you've thought about
```

## 🎯 Good First Issues

Look for issues labeled:
- `good first issue`
- `help wanted`
- `documentation`

## 🔧 Areas for Contribution

### High Priority:

- [ ] Unit tests for core modules
- [ ] Web interface (Flask/FastAPI)
- [ ] More document format processors
- [ ] Enhanced error handling
- [ ] Performance optimizations

### Medium Priority:

- [ ] Plugin system
- [ ] Scheduled tasks
- [ ] Undo system improvements
- [ ] Multi-workspace support

### Documentation:

- [ ] Video tutorials
- [ ] More examples
- [ ] Translation to other languages
- [ ] API documentation

## 📚 Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Project Architecture](ARCHITECTURE.md)
- [Examples](EXAMPLES.md)

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior:

- ✅ Be respectful and inclusive
- ✅ Accept constructive criticism
- ✅ Focus on what's best for the project
- ✅ Show empathy towards others

### Unacceptable Behavior:

- ❌ Harassment or discrimination
- ❌ Trolling or insulting comments
- ❌ Personal or political attacks
- ❌ Publishing others' private information

## 📞 Getting Help

- 💬 Open a discussion on GitHub
- 📧 Contact maintainers
- 📖 Read the documentation

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to Local Helper! 🚀
