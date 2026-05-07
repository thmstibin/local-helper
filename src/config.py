"""Configuration management for Local Helper."""
import os
from pathlib import Path
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # API Configuration
    anthropic_api_key: str = Field(..., validation_alias="ANTHROPIC_API_KEY")
    model_name: str = Field(default="claude-3-5-sonnet-20241022", validation_alias="MODEL_NAME")
    max_tokens: int = Field(default=4096, validation_alias="MAX_TOKENS")
    temperature: float = Field(default=0.7, validation_alias="TEMPERATURE")

    # Workspace Configuration
    workspace_path: Path = Field(..., validation_alias="WORKSPACE_PATH")
    max_file_size_mb: int = Field(default=50, validation_alias="MAX_FILE_SIZE_MB")

    # Safety Configuration
    enable_undo: bool = Field(default=True, validation_alias="ENABLE_UNDO")
    backup_enabled: bool = Field(default=True, validation_alias="BACKUP_ENABLED")
    backup_path: Path = Field(default=Path("./.backups"), validation_alias="BACKUP_PATH")

    # Logging
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    log_file: Path = Field(default=Path("./local_helper.log"), validation_alias="LOG_FILE")

    @field_validator("workspace_path", "backup_path", mode="before")
    @classmethod
    def convert_to_path(cls, v):
        """Convert string paths to Path objects."""
        if isinstance(v, str):
            return Path(v).expanduser().resolve()
        return v

    @field_validator("workspace_path")
    @classmethod
    def validate_workspace(cls, v):
        """Ensure workspace exists or can be created."""
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        return v


def load_config() -> Config:
    """Load configuration from environment."""
    return Config(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        workspace_path=os.getenv("WORKSPACE_PATH", "./workspace"),
    )
