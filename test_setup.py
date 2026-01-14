#!/usr/bin/env python3
"""Test script to verify Local Helper installation."""
import sys
from pathlib import Path

def test_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (need 3.9+)")
        return False

def test_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking dependencies...")
    required = [
        'anthropic',
        'rich',
        'pydantic',
        'dotenv',
        'PyPDF2',
        'openpyxl',
        'docx'
    ]
    
    all_installed = True
    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'docx':
                __import__('docx')
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (not installed)")
            all_installed = False
    
    return all_installed

def test_env_file():
    """Check if .env file exists."""
    print("\n⚙️  Checking configuration...")
    env_file = Path('.env')
    
    if env_file.exists():
        print("   ✅ .env file exists")
        
        # Check for API key
        with open(env_file) as f:
            content = f.read()
            if 'ANTHROPIC_API_KEY' in content and 'your_api_key_here' not in content:
                print("   ✅ API key configured")
                return True
            else:
                print("   ⚠️  API key not configured (edit .env)")
                return False
    else:
        print("   ❌ .env file not found")
        print("      Run: cp .env.example .env")
        return False

def test_workspace():
    """Check workspace configuration."""
    print("\n📁 Checking workspace...")
    
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        workspace = os.getenv('WORKSPACE_PATH', './workspace')
        workspace_path = Path(workspace).expanduser()
        
        if workspace_path.exists():
            print(f"   ✅ Workspace exists: {workspace_path}")
            return True
        else:
            print(f"   ⚠️  Workspace doesn't exist: {workspace_path}")
            print(f"      Creating workspace...")
            workspace_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Workspace created")
            return True
    except Exception as e:
        print(f"   ❌ Error checking workspace: {e}")
        return False

def test_imports():
    """Test importing Local Helper modules."""
    print("\n🔧 Testing Local Helper modules...")
    
    try:
        from src.config import Config
        print("   ✅ config module")
        
        from src.models import Task, TaskStatus
        print("   ✅ models module")
        
        from src.file_operations import FileOperations
        print("   ✅ file_operations module")
        
        from src.task_executor import TaskExecutor
        print("   ✅ task_executor module")
        
        from src.document_processor import DocumentProcessor
        print("   ✅ document_processor module")
        
        from src.agent import LocalHelperAgent
        print("   ✅ agent module")
        
        from src.cli import CLI
        print("   ✅ cli module")
        
        return True
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Local Helper - Installation Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Python Version", test_python_version()))
    results.append(("Dependencies", test_dependencies()))
    results.append(("Configuration", test_env_file()))
    results.append(("Workspace", test_workspace()))
    results.append(("Modules", test_imports()))
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! You're ready to use Local Helper.")
        print("\nRun: python main.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nSee SETUP_GUIDE.md for detailed instructions.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

