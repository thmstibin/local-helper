"""Task execution engine."""
import logging
import asyncio
from typing import Dict, Any, List
from pathlib import Path
import re

from .config import Config
from .models import AgentAction
from .file_operations import FileOperations
from .document_processor import DocumentProcessor

logger = logging.getLogger(__name__)


class TaskExecutor:
    """Executes agent actions on files."""

    def __init__(self, config: Config, file_ops: FileOperations):
        """Initialize task executor.

        Args:
            config: Application configuration
            file_ops: File operations handler
        """
        self.config = config
        self.file_ops = file_ops
        self.doc_processor = DocumentProcessor(config, file_ops)

    async def execute_action(self, action: AgentAction) -> Dict[str, Any]:
        """Execute a single action.

        Args:
            action: Action to execute

        Returns:
            Result of the action
        """
        action_type = action.action_type.lower()

        handlers = {
            "read_file": self._handle_read_file,
            "write_file": self._handle_write_file,
            "organize_files": self._handle_organize_files,
            "extract_data": self._handle_extract_data,
            "generate_report": self._handle_generate_report,
            "search_files": self._handle_search_files,
            "batch_process": self._handle_batch_process,
            "delete_file": self._handle_delete_file,
            "move_file": self._handle_move_file,
            "copy_file": self._handle_copy_file,
        }

        handler = handlers.get(action_type)
        if not handler:
            raise ValueError(f"Unknown action type: {action_type}")

        return await handler(action)

    async def _handle_read_file(self, action: AgentAction) -> Dict[str, Any]:
        """Handle file reading."""
        results = {}
        for file_path in action.target_files:
            try:
                content = self.file_ops.read_file(file_path)
                results[str(file_path)] = {
                    "success": True,
                    "content": content[:1000],  # Truncate for logging
                    "size": len(content)
                }
            except Exception as e:
                results[str(file_path)] = {"success": False, "error": str(e)}
        return results

    async def _handle_write_file(self, action: AgentAction) -> Dict[str, Any]:
        """Handle file writing."""
        file_path = action.target_files[0] if action.target_files else Path(action.parameters.get("filename", "output.txt"))
        content = action.parameters.get("content", "")

        written_path = self.file_ops.write_file(file_path, content)
        return {
            "success": True,
            "file": str(written_path),
            "size": len(content)
        }

    async def _handle_delete_file(self, action: AgentAction) -> Dict[str, Any]:
        """Handle file deletion."""
        results = {}
        for file_path in action.target_files:
            try:
                deleted = self.file_ops.delete_file(file_path)
                results[str(file_path)] = {"success": deleted}
            except Exception as e:
                results[str(file_path)] = {"success": False, "error": str(e)}
        return results

    async def _handle_move_file(self, action: AgentAction) -> Dict[str, Any]:
        """Handle file moving."""
        source = action.target_files[0]
        destination = Path(action.parameters.get("destination", ""))

        new_path = self.file_ops.move_file(source, destination)
        return {
            "success": True,
            "source": str(source),
            "destination": str(new_path)
        }

    async def _handle_copy_file(self, action: AgentAction) -> Dict[str, Any]:
        """Handle file copying."""
        source = action.target_files[0]
        destination = Path(action.parameters.get("destination", ""))

        new_path = self.file_ops.copy_file(source, destination)
        return {
            "success": True,
            "source": str(source),
            "destination": str(new_path)
        }

    async def _handle_organize_files(self, action: AgentAction) -> Dict[str, Any]:
        """Handle file organization."""
        criteria = action.parameters.get("criteria", "type")
        pattern = action.parameters.get("pattern", "*")

        files = self.file_ops.list_files(pattern)
        organized = {"moved": 0, "errors": []}

        for file_path in files:
            try:
                if criteria == "type":
                    # Organize by file extension
                    ext = file_path.suffix.lstrip('.') or "no_extension"
                    dest = Path(ext) / file_path.name
                    self.file_ops.move_file(file_path, dest)
                    organized["moved"] += 1
                elif criteria == "date":
                    # Organize by modification date
                    full_path = self.config.workspace_path / file_path
                    mtime = full_path.stat().st_mtime
                    from datetime import datetime
                    date_folder = datetime.fromtimestamp(mtime).strftime("%Y-%m")
                    dest = Path(date_folder) / file_path.name
                    self.file_ops.move_file(file_path, dest)
                    organized["moved"] += 1
            except Exception as e:
                organized["errors"].append({"file": str(file_path), "error": str(e)})

        return organized

    async def _handle_extract_data(self, action: AgentAction) -> Dict[str, Any]:
        """Handle data extraction from documents."""
        results = {"extracted": []}

        for file_path in action.target_files:
            try:
                data = await self.doc_processor.extract_data(file_path)
                results["extracted"].append({
                    "file": str(file_path),
                    "data": data
                })
            except Exception as e:
                results["extracted"].append({
                    "file": str(file_path),
                    "error": str(e)
                })

        return results

    async def _handle_generate_report(self, action: AgentAction) -> Dict[str, Any]:
        """Handle report generation."""
        report_type = action.parameters.get("report_type", "summary")
        output_file = Path(action.parameters.get("output_file", "report.txt"))

        # Collect data from target files
        data_points = []
        for file_path in action.target_files:
            try:
                content = self.file_ops.read_file(file_path)
                data_points.append({
                    "file": str(file_path),
                    "content": content
                })
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")

        # Generate report content
        report_content = self._generate_report_content(report_type, data_points, action.parameters)

        # Write report
        self.file_ops.write_file(output_file, report_content)

        return {
            "success": True,
            "report_file": str(output_file),
            "files_processed": len(data_points)
        }

    async def _handle_search_files(self, action: AgentAction) -> Dict[str, Any]:
        """Handle file searching."""
        query = action.parameters.get("query", "")
        pattern = action.parameters.get("pattern", "*")
        search_content = action.parameters.get("search_content", False)

        files = self.file_ops.list_files(pattern)
        matches = []

        for file_path in files:
            # Search in filename
            if query.lower() in str(file_path).lower():
                matches.append({
                    "file": str(file_path),
                    "match_type": "filename"
                })
                continue

            # Search in content if requested
            if search_content:
                try:
                    content = self.file_ops.read_file(file_path)
                    if query.lower() in content.lower():
                        matches.append({
                            "file": str(file_path),
                            "match_type": "content"
                        })
                except Exception:
                    pass  # Skip files that can't be read

        return {
            "query": query,
            "matches": matches,
            "total_matches": len(matches)
        }

    async def _handle_batch_process(self, action: AgentAction) -> Dict[str, Any]:
        """Handle batch processing of files."""
        operation = action.parameters.get("operation", "")
        results = {"processed": 0, "errors": []}

        for file_path in action.target_files:
            try:
                if operation == "rename":
                    # Batch rename with pattern
                    new_name = action.parameters.get("new_name_pattern", "")
                    new_path = file_path.parent / new_name.replace("{name}", file_path.stem).replace("{ext}", file_path.suffix)
                    self.file_ops.move_file(file_path, new_path)
                    results["processed"] += 1
                elif operation == "convert":
                    # Placeholder for format conversion
                    results["processed"] += 1
            except Exception as e:
                results["errors"].append({"file": str(file_path), "error": str(e)})

        return results

    def _generate_report_content(self, report_type: str, data_points: List[Dict], params: Dict) -> str:
        """Generate report content based on type."""
        if report_type == "summary":
            lines = ["# File Summary Report\n"]
            lines.append(f"Generated: {params.get('timestamp', 'now')}\n")
            lines.append(f"\nTotal files processed: {len(data_points)}\n\n")

            for item in data_points:
                lines.append(f"## {item['file']}\n")
                lines.append(f"Size: {len(item['content'])} characters\n")
                lines.append(f"Preview: {item['content'][:200]}...\n\n")

            return "".join(lines)

        elif report_type == "list":
            lines = ["# File List\n\n"]
            for item in data_points:
                lines.append(f"- {item['file']}\n")
            return "".join(lines)

        else:
            return f"Report type '{report_type}' not implemented yet."
