"""Configuration management for Local Helper."""
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

load_dotenv()


class Config(BaseModel):
    """Application configuration."""
    
    # API Configuration
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    model_name: str = Field(default="claude-3-5-sonnet-20241022", env="MODEL_NAME")
    max_tokens: int = Field(default=4096, env="MAX_TOKENS")
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    
    # Workspace Configuration
    workspace_path: Path = Field(..., env="WORKSPACE_PATH")
    max_file_size_mb: int = Field(default=50, env="MAX_FILE_SIZE_MB")
    
    # Safety Configuration
    enable_undo: bool = Field(default=True, env="ENABLE_UNDO")
    backup_enabled: bool = Field(default=True, env="BACKUP_ENABLED")
    backup_path: Path = Field(default=Path("./.backups"), env="BACKUP_PATH")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Path = Field(default=Path("./local_helper.log"), env="LOG_FILE")
    
    @validator("workspace_path", "backup_path", pre=True)
    def convert_to_path(cls, v):
        """Convert string paths to Path objects."""
        if isinstance(v, str):
            return Path(v).expanduser().resolve()
        return v
    
    @validator("workspace_path")
    def validate_workspace(cls, v):
        """Ensure workspace exists or can be created."""
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_config() -> Config:
    """Load configuration from environment."""
    return Config(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        workspace_path=os.getenv("WORKSPACE_PATH", "./workspace"),
    )

