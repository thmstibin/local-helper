"""Safe file operations with sandboxing and backup."""
import os
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib
import json

from .config import Config
from .models import FileOperation

logger = logging.getLogger(__name__)


class FileOperations:
    """Handles all file operations with safety checks."""
    
    def __init__(self, config: Config):
        """Initialize file operations handler.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.workspace = config.workspace_path
        self.backup_path = config.backup_path
        self.operation_history: List[Dict[str, Any]] = []
        
        # Ensure backup directory exists
        if config.backup_enabled:
            self.backup_path.mkdir(parents=True, exist_ok=True)
    
    def _is_safe_path(self, path: Path) -> bool:
        """Check if path is within workspace (prevent directory traversal).
        
        Args:
            path: Path to check
            
        Returns:
            True if path is safe
        """
        try:
            resolved = path.resolve()
            workspace_resolved = self.workspace.resolve()
            return resolved.is_relative_to(workspace_resolved)
        except (ValueError, RuntimeError):
            return False
    
    def _create_backup(self, file_path: Path) -> Optional[Path]:
        """Create a backup of a file before modification.
        
        Args:
            file_path: File to backup
            
        Returns:
            Path to backup file
        """
        if not self.config.backup_enabled or not file_path.exists():
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.backup"
        backup_file = self.backup_path / backup_name
        
        shutil.copy2(file_path, backup_file)
        logger.info(f"Created backup: {backup_file}")
        return backup_file
    
    def _log_operation(self, operation: FileOperation, path: Path, details: Dict[str, Any]):
        """Log a file operation for undo capability.
        
        Args:
            operation: Type of operation
            path: File path
            details: Additional details
        """
        self.operation_history.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation.value,
            "path": str(path),
            "details": details
        })
    
    def read_file(self, file_path: Path) -> str:
        """Read file contents safely.
        
        Args:
            file_path: Path to file
            
        Returns:
            File contents
        """
        full_path = self.workspace / file_path
        
        if not self._is_safe_path(full_path):
            raise ValueError(f"Path outside workspace: {file_path}")
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check file size
        size_mb = full_path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_file_size_mb:
            raise ValueError(f"File too large: {size_mb:.2f}MB (max: {self.config.max_file_size_mb}MB)")
        
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        self._log_operation(FileOperation.READ, file_path, {"size": full_path.stat().st_size})
        return content
    
    def write_file(self, file_path: Path, content: str, create_backup: bool = True) -> Path:
        """Write content to file safely.
        
        Args:
            file_path: Path to file
            content: Content to write
            create_backup: Whether to create backup if file exists
            
        Returns:
            Path to written file
        """
        full_path = self.workspace / file_path
        
        if not self._is_safe_path(full_path):
            raise ValueError(f"Path outside workspace: {file_path}")
        
        # Create parent directories
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Backup existing file
        backup_file = None
        if create_backup and full_path.exists():
            backup_file = self._create_backup(full_path)
        
        # Write file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self._log_operation(FileOperation.WRITE, file_path, {
            "size": len(content),
            "backup": str(backup_file) if backup_file else None
        })
        
        logger.info(f"Wrote file: {full_path}")
        return full_path
    
    def create_file(self, file_path: Path, content: str = "") -> Path:
        """Create a new file.
        
        Args:
            file_path: Path to new file
            content: Initial content
            
        Returns:
            Path to created file
        """
        return self.write_file(file_path, content, create_backup=False)

    def delete_file(self, file_path: Path, create_backup: bool = True) -> bool:
        """Delete a file safely.

        Args:
            file_path: Path to file
            create_backup: Whether to create backup before deletion

        Returns:
            True if deleted
        """
        full_path = self.workspace / file_path

        if not self._is_safe_path(full_path):
            raise ValueError(f"Path outside workspace: {file_path}")

        if not full_path.exists():
            return False

        # Backup before deletion
        backup_file = None
        if create_backup:
            backup_file = self._create_backup(full_path)

        full_path.unlink()
        self._log_operation(FileOperation.DELETE, file_path, {
            "backup": str(backup_file) if backup_file else None
        })

        logger.info(f"Deleted file: {full_path}")
        return True

    def move_file(self, source: Path, destination: Path) -> Path:
        """Move a file to a new location.

        Args:
            source: Source file path
            destination: Destination path

        Returns:
            New file path
        """
        src_full = self.workspace / source
        dst_full = self.workspace / destination

        if not self._is_safe_path(src_full) or not self._is_safe_path(dst_full):
            raise ValueError("Path outside workspace")

        if not src_full.exists():
            raise FileNotFoundError(f"Source file not found: {source}")

        # Create destination directory
        dst_full.parent.mkdir(parents=True, exist_ok=True)

        # Backup if destination exists
        if dst_full.exists():
            self._create_backup(dst_full)

        shutil.move(str(src_full), str(dst_full))
        self._log_operation(FileOperation.MOVE, source, {"destination": str(destination)})

        logger.info(f"Moved file: {source} -> {destination}")
        return dst_full

    def copy_file(self, source: Path, destination: Path) -> Path:
        """Copy a file to a new location.

        Args:
            source: Source file path
            destination: Destination path

        Returns:
            New file path
        """
        src_full = self.workspace / source
        dst_full = self.workspace / destination

        if not self._is_safe_path(src_full) or not self._is_safe_path(dst_full):
            raise ValueError("Path outside workspace")

        if not src_full.exists():
            raise FileNotFoundError(f"Source file not found: {source}")

        dst_full.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src_full), str(dst_full))

        self._log_operation(FileOperation.COPY, source, {"destination": str(destination)})
        logger.info(f"Copied file: {source} -> {destination}")
        return dst_full

    def list_files(self, pattern: str = "*", recursive: bool = True) -> List[Path]:
        """List files in workspace matching pattern.

        Args:
            pattern: Glob pattern
            recursive: Whether to search recursively

        Returns:
            List of matching file paths
        """
        if recursive:
            files = list(self.workspace.rglob(pattern))
        else:
            files = list(self.workspace.glob(pattern))

        # Return relative paths
        return [f.relative_to(self.workspace) for f in files if f.is_file()]

    def get_workspace_summary(self) -> Dict[str, Any]:
        """Get summary information about the workspace.

        Returns:
            Workspace summary
        """
        files = list(self.workspace.rglob("*"))
        file_list = [f for f in files if f.is_file()]

        # Get file types
        extensions = set(f.suffix for f in file_list if f.suffix)

        # Calculate total size
        total_size = sum(f.stat().st_size for f in file_list)

        # Get recent files
        recent_files = sorted(file_list, key=lambda f: f.stat().st_mtime, reverse=True)[:10]

        return {
            "path": str(self.workspace),
            "file_count": len(file_list),
            "file_types": sorted(extensions),
            "total_size": self._format_size(total_size),
            "recent_files": [
                {
                    "name": str(f.relative_to(self.workspace)),
                    "size": self._format_size(f.stat().st_size),
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                }
                for f in recent_files
            ]
        }

    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"

    def get_operation_history(self) -> List[Dict[str, Any]]:
        """Get history of file operations."""
        return self.operation_history.copy()

