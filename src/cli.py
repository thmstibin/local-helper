"""Command-line interface for Local Helper."""
import asyncio
import logging
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown

from .config import load_config
from .agent import LocalHelperAgent
from .models import ProgressUpdate, TaskStatus

console = Console()


class CLI:
    """Command-line interface for Local Helper."""
    
    def __init__(self):
        """Initialize CLI."""
        self.config = None
        self.agent = None
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('local_helper.log'),
                logging.StreamHandler()
            ]
        )
    
    def display_welcome(self):
        """Display welcome message."""
        welcome_text = """
# 🤖 Local Helper

An autonomous AI assistant that helps with file management and productivity tasks.

**Features:**
- 📁 File organization and management
- 📄 Document processing (PDF, Excel, Word, etc.)
- 🔍 Smart file search
- 📊 Report generation
- ⚡ Batch operations
- 🔒 Safe operations with backup

Type your request in natural language, and I'll handle the rest!
        """
        console.print(Panel(Markdown(welcome_text), border_style="blue"))
    
    def display_workspace_info(self):
        """Display workspace information."""
        if not self.config:
            return
        
        table = Table(title="Workspace Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Workspace Path", str(self.config.workspace_path))
        table.add_row("Backup Enabled", "Yes" if self.config.backup_enabled else "No")
        table.add_row("Max File Size", f"{self.config.max_file_size_mb}MB")
        table.add_row("Model", self.config.model_name)
        
        console.print(table)
    
    def progress_callback(self, update: ProgressUpdate):
        """Handle progress updates from agent.
        
        Args:
            update: Progress update
        """
        status_colors = {
            TaskStatus.PLANNING: "yellow",
            TaskStatus.IN_PROGRESS: "blue",
            TaskStatus.COMPLETED: "green",
            TaskStatus.FAILED: "red"
        }
        
        color = status_colors.get(update.status, "white")
        
        console.print(
            f"[{color}]●[/{color}] [{update.current_step}/{update.total_steps}] {update.message}"
        )
    
    async def run_interactive(self):
        """Run interactive mode."""
        self.display_welcome()
        
        # Load configuration
        try:
            self.config = load_config()
            console.print("[green]✓[/green] Configuration loaded")
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to load configuration: {e}")
            console.print("\nPlease create a .env file with your configuration.")
            console.print("See .env.example for reference.")
            return
        
        self.display_workspace_info()
        
        # Initialize agent
        self.agent = LocalHelperAgent(self.config, progress_callback=self.progress_callback)
        console.print("[green]✓[/green] Agent initialized\n")
        
        # Main loop
        while True:
            try:
                console.print()
                user_input = Prompt.ask("[bold cyan]What would you like me to do?[/bold cyan]")
                
                if not user_input.strip():
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break
                
                # Check for help
                if user_input.lower() in ['help', '?']:
                    self.display_help()
                    continue
                
                # Execute task
                console.print()
                task = await self.agent.execute_task(user_input)
                
                # Display results
                self.display_task_result(task)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                logging.exception("Error in interactive mode")
    
    def display_help(self):
        """Display help information."""
        help_text = """
## Available Commands

**File Operations:**
- "Organize my files by type"
- "Find all PDF files"
- "Create a summary of all text files"
- "Move all images to a Photos folder"

**Document Processing:**
- "Extract data from expenses.xlsx"
- "Create a report from all CSV files"
- "Summarize document.pdf"

**Search:**
- "Find files containing 'budget'"
- "List all files modified this week"

**Other Commands:**
- `help` or `?` - Show this help
- `exit` or `quit` - Exit the program
        """
        console.print(Panel(Markdown(help_text), title="Help", border_style="cyan"))

    def display_task_result(self, task):
        """Display task execution results.

        Args:
            task: Completed task
        """
        console.print()

        if task.status == TaskStatus.COMPLETED:
            console.print(Panel(
                f"[green]✓ Task completed successfully![/green]\n\n"
                f"Steps executed: {len(task.steps)}\n"
                f"Duration: {(task.completed_at - task.started_at).total_seconds():.1f}s",
                title="Success",
                border_style="green"
            ))

            # Display results if available
            if task.result:
                console.print("\n[bold]Results:[/bold]")
                self._display_result_details(task.result)

        elif task.status == TaskStatus.FAILED:
            console.print(Panel(
                f"[red]✗ Task failed[/red]\n\n"
                f"Error: {task.error}",
                title="Failed",
                border_style="red"
            ))

    def _display_result_details(self, result: dict, indent: int = 0):
        """Display result details recursively."""
        prefix = "  " * indent

        for key, value in result.items():
            if isinstance(value, dict):
                console.print(f"{prefix}[cyan]{key}:[/cyan]")
                self._display_result_details(value, indent + 1)
            elif isinstance(value, list):
                console.print(f"{prefix}[cyan]{key}:[/cyan] ({len(value)} items)")
                for item in value[:5]:  # Show first 5 items
                    if isinstance(item, dict):
                        self._display_result_details(item, indent + 1)
                    else:
                        console.print(f"{prefix}  - {item}")
                if len(value) > 5:
                    console.print(f"{prefix}  ... and {len(value) - 5} more")
            else:
                console.print(f"{prefix}[cyan]{key}:[/cyan] {value}")


async def main():
    """Main entry point."""
    cli = CLI()
    await cli.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())

