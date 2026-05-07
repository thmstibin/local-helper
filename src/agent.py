"""Core autonomous agent implementation."""
import json
import logging
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime
from anthropic import Anthropic
from pathlib import Path

from .models import Task, TaskStatus, AgentPlan, AgentAction, ProgressUpdate
from .config import Config
from .file_operations import FileOperations
from .task_executor import TaskExecutor

logger = logging.getLogger(__name__)


class LocalHelperAgent:
    """Autonomous agent that executes tasks using Claude API."""

    def __init__(self, config: Config, progress_callback: Optional[Callable] = None):
        """Initialize the agent.

        Args:
            config: Application configuration
            progress_callback: Optional callback for progress updates
        """
        self.config = config
        self.client = Anthropic(api_key=config.anthropic_api_key)
        self.file_ops = FileOperations(config)
        self.executor = TaskExecutor(config, self.file_ops)
        self.progress_callback = progress_callback
        self.current_task: Optional[Task] = None

    def _send_progress(self, update: ProgressUpdate):
        """Send progress update to callback."""
        if self.progress_callback:
            self.progress_callback(update)
        logger.info(f"Progress: {update.message}")

    async def execute_task(self, user_request: str) -> Task:
        """Execute a task based on user's natural language request.

        Args:
            user_request: Natural language description of the task

        Returns:
            Completed task with results
        """
        # Create task
        task = Task(description=user_request)
        self.current_task = task

        try:
            # Step 1: Plan the task
            task.status = TaskStatus.PLANNING
            self._send_progress(ProgressUpdate(
                task_id=task.id,
                status=task.status,
                current_step=0,
                total_steps=3,
                message="Planning task execution..."
            ))

            plan = await self._create_plan(user_request)
            task.steps = [action.description for action in plan.actions]

            # Step 2: Execute the plan
            task.status = TaskStatus.IN_PROGRESS
            task.started_at = datetime.now()

            results = await self._execute_plan(task, plan)

            # Step 3: Complete
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = results

            self._send_progress(ProgressUpdate(
                task_id=task.id,
                status=task.status,
                current_step=len(task.steps),
                total_steps=len(task.steps),
                message="Task completed successfully!"
            ))

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            logger.error(f"Task failed: {e}", exc_info=True)
            self._send_progress(ProgressUpdate(
                task_id=task.id,
                status=task.status,
                current_step=task.current_step,
                total_steps=len(task.steps),
                message=f"Task failed: {str(e)}"
            ))

        return task

    async def _create_plan(self, user_request: str) -> AgentPlan:
        """Create an execution plan using Claude.

        Args:
            user_request: User's natural language request

        Returns:
            Execution plan with actions
        """
        # Get workspace context
        workspace_info = self.file_ops.get_workspace_summary()

        system_prompt = self._build_system_prompt()
        user_prompt = self._build_planning_prompt(user_request, workspace_info)

        response = self.client.messages.create(
            model=self.config.model_name,
            max_tokens=self.config.max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        # Parse the plan from Claude's response
        plan_data = self._parse_plan_response(response.content[0].text)
        return AgentPlan(**plan_data)

    async def _execute_plan(self, task: Task, plan: AgentPlan) -> Dict[str, Any]:
        """Execute the planned actions.

        Args:
            task: The task being executed
            plan: The execution plan

        Returns:
            Results of execution
        """
        results = {"actions_completed": [], "files_modified": []}

        for idx, action in enumerate(plan.actions):
            task.current_step = idx + 1
            self._send_progress(ProgressUpdate(
                task_id=task.id,
                status=task.status,
                current_step=task.current_step,
                total_steps=len(plan.actions),
                message=f"Executing: {action.description}"
            ))

            # Execute the action
            action_result = await self.executor.execute_action(action)
            results["actions_completed"].append({
                "action": action.description,
                "result": action_result
            })

            if action.target_files:
                results["files_modified"].extend([str(f) for f in action.target_files])

        return results

    def _build_system_prompt(self) -> str:
        """Build the system prompt for Claude."""
        return """You are an autonomous AI assistant that helps users with file management and productivity tasks.

You have access to a workspace folder where you can:
- Read, create, edit, and organize files
- Process documents (PDF, Excel, Word, text files)
- Extract and analyze data
- Generate reports and summaries
- Automate repetitive file operations

When given a task, you should:
1. Analyze what needs to be done
2. Create a detailed plan with specific actions
3. Return your plan in JSON format

Your response must be valid JSON with this structure:
{
  "task_id": "unique_id",
  "goal": "clear description of what you'll accomplish",
  "actions": [
    {
      "action_type": "file_operation_type",
      "description": "what this action does",
      "target_files": ["list", "of", "file", "paths"],
      "parameters": {"key": "value"},
      "requires_confirmation": false
    }
  ],
  "estimated_duration": "approximate time",
  "risks": ["potential issues to be aware of"]
}

Available action types:
- read_file: Read file contents
- write_file: Create or update a file
- organize_files: Move/rename files based on criteria
- extract_data: Extract information from documents
- generate_report: Create a new document with analysis
- search_files: Find files matching criteria
- batch_process: Apply operation to multiple files

Be specific and thorough in your planning."""

    def _build_planning_prompt(self, user_request: str, workspace_info: Dict[str, Any]) -> str:
        """Build the planning prompt with context."""
        return f"""User Request: {user_request}

Workspace Information:
- Location: {workspace_info['path']}
- Total Files: {workspace_info['file_count']}
- File Types: {', '.join(workspace_info['file_types'])}
- Total Size: {workspace_info['total_size']}

Recent Files:
{self._format_file_list(workspace_info.get('recent_files', []))}

Please create a detailed execution plan for this request. Return only valid JSON."""

    def _format_file_list(self, files: List[Dict[str, Any]]) -> str:
        """Format file list for display."""
        if not files:
            return "No files found"
        return "\n".join([f"- {f['name']} ({f['size']}, modified: {f['modified']})" for f in files[:10]])

    def _parse_plan_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude's JSON response into a plan."""
        try:
            # Extract JSON from response (handle markdown code blocks)
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]

            plan_data = json.loads(text.strip())

            # Convert string paths to Path objects
            for action in plan_data.get("actions", []):
                action["target_files"] = [Path(f) for f in action.get("target_files", [])]

            return plan_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse plan response: {e}")
            # Return a basic plan if parsing fails
            return {
                "task_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "goal": "Execute user request",
                "actions": [],
                "estimated_duration": "Unknown",
                "risks": ["Failed to parse detailed plan"]
            }
