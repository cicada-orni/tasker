import typer
from tasker.storage import TaskStorage
from tasker.services import TaskService
from tasker.models import Task

app = typer.Typer()

@app.callback()
def main(ctx: typer.Context):
    """
    CLI Task App
    """
    storage = TaskStorage()
    service = TaskService(storage)
    ctx.obj = service

@app.command()
def add(ctx: typer.Context, title: str):
    service: TaskService = ctx.obj
    service.create_task(title=title)
    print(f"{title} task created successfull.")

@app.command("list")
def display(ctx: typer.Context):
    service: TaskService = ctx.obj
    tasks_list = service.list_tasks()
    for task in tasks_list:
        print(task.title)




