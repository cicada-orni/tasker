import typer
from tasker.storage import TaskStorage
from tasker.services import TaskService
from tasker.models import Task, Status, Priority
from typing import Annotated
from rich.console import Console
from rich.table import Table
from tasker.exceptions import TaskNotFoundError


app = typer.Typer()
console = Console()

@app.callback()
def main(ctx: typer.Context):
    """
    CLI Task App
    """
    storage = TaskStorage()
    service = TaskService(storage)
    ctx.obj = service
# ADD
@app.command()
def add(ctx: typer.Context,  title: Annotated[str, typer.Argument(help='The name of the task')], description: Annotated[str | None, typer.Option(help="Task description")] = None, status: Annotated[str | None, typer.Option(help="Task status")] = None, priority: Annotated[str | None, typer.Option(help="Task priority")] = None, due_date: Annotated[str | None, typer.Option(help="Task due date")] = None, tags: Annotated[str | None, typer.Option(help="Task tags")] = None ):
    service: TaskService = ctx.obj
    task_args = {'title': title, 'description': description, 'status': status, 'priority': priority, 'due_date': due_date, 'tags': tags}
    cleaned_task_args = {k: v for k, v in task_args.items() if v is not None}
    service.create_task(**cleaned_task_args)
    print(f"{title} task created successfully.")

# DELETE
@app.command()
def delete(ctx: typer.Context, task_id: str):
    service: TaskService = ctx.obj
    try:
        task = service.delete_task(task_id)
        console.print(f"\n[bold green]✓[/bold green] Deleted Task: [white]{task.title}[/white] [dim]({str(task.task_id)[:8]})[/dim]")
    except TaskNotFoundError:
        console.print(f"\n[bold red]❌ Error:[/bold red] No task found starting with [yellow]'{task_id}'[/yellow]")
        raise typer.Exit(code=1)
    
    except ValueError as e:
        # This handles the "Ambiguous ID" case
        console.print(f"\n[bold yellow]⚠ {e}[/bold yellow]")
        console.print("Please provide more characters of the UUID to be specific.")
        raise typer.Exit(code=1)


@app.command("list")
def list_tasks(ctx: typer.Context):
    service: TaskService = ctx.obj
    tasks: list[Task] = service.list_tasks()
    
    if not tasks:
        console.print("\n[yellow]⚠ No tasks found. Use 'add' to create one.[/yellow]")
        return
    
    # Table Creation
    table = Table(
        title="[bold cyan]Task Manager Dashboard[/bold cyan]",
        header_style="bold magenta",
        show_lines=True
    )

    # Define Columns
    table.add_column("ID", style="dim", width=8)
    table.add_column("Title", style="bold white")
    table.add_column("Status", justify="center")
    table.add_column("Priority", justify="center")
    table.add_column("Created At", style="italic blue", justify="right")

    for task in tasks:
        # Color logic for status
        status_color = "green" if task.status == Status.Done else "yellow"
        if task.status == Status.In_Progress:
            status_color = "orange3"

        # Color logic for priority
        priority_color = "white"
        if task.priority == Priority.High:
            priority_color = 'red'
        elif task.priority == Priority.Medium:
            priority_color = 'yellow'

        table.add_row(
            str(task.task_id)[:8],
            task.title,
            f"[{status_color}]{task.status}[/{status_color}]",
            f"[{priority_color}]{task.priority}[/{priority_color}]",
            task.created_at.strftime("%b %d, %H:%M")
        )
        
    console.print(table)







