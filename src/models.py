"""Data models for Local Helper."""
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from pathlib import Path


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(str, Enum):
    """Types of tasks the agent can perform."""
    FILE_ORGANIZATION = "file_organization"
    DOCUMENT_PROCESSING = "document_processing"
    DATA_EXTRACTION = "data_extraction"
    REPORT_GENERATION = "report_generation"
    FILE_SEARCH = "file_search"
    BATCH_OPERATION = "batch_operation"
    CUSTOM = "custom"


class FileOperation(str, Enum):
    """File operation types."""
    READ = "read"
    WRITE = "write"
    CREATE = "create"
    DELETE = "delete"
    MOVE = "move"
    COPY = "copy"
    RENAME = "rename"


class Task(BaseModel):
    """Represents a task to be executed."""
    id: str = Field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    description: str
    task_type: TaskType = TaskType.CUSTOM
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    steps: List[str] = Field(default_factory=list)
    current_step: int = 0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    files_affected: List[Path] = Field(default_factory=list)


class AgentAction(BaseModel):
    """Represents an action the agent plans to take."""
    action_type: str
    description: str
    target_files: List[Path] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    requires_confirmation: bool = False


class AgentPlan(BaseModel):
    """Represents the agent's execution plan."""
    task_id: str
    goal: str
    actions: List[AgentAction]
    estimated_duration: Optional[str] = None
    risks: List[str] = Field(default_factory=list)


class ProgressUpdate(BaseModel):
    """Progress update for a task."""
    task_id: str
    status: TaskStatus
    current_step: int
    total_steps: int
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

