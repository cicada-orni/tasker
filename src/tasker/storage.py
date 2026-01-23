from abc import ABC, abstractmethod
from tasker.models import Task
from uuid import UUID
from tasker.exceptions import TaskNotFoundError, TaskAlreadyExistsError
from pathlib import Path
from pydantic import TypeAdapter


class Storage(ABC):
    @abstractmethod
    def add_task(self, task: Task) -> None:
        pass

    @abstractmethod
    def get_task(self, task_id: UUID) -> Task:
        pass

    @abstractmethod
    def list_tasks(self) -> list[Task]:
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> Task:
        pass


class TaskStorage(Storage):
    def __init__(self) -> None:
        path = Path.home() / ".tasker" / "tasks.json"
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        self._file_path = path
        if self._file_path.is_file() and self._file_path.stat().st_size > 0:
            self._tasks: dict[UUID, Task] = self._load()
        else:
            self._tasks: dict[UUID, Task] = {}
    # CREATE
    def add_task(self, task: Task) -> None:
        if task.task_id in self._tasks:
            raise TaskAlreadyExistsError(task.task_id)
        self._tasks[task.task_id] = task
        self._save()

    # READ
    def get_task(self, task_id: UUID) -> Task:
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]
    
    # DELETE
    def delete_task(self, task_id: str) -> Task:
        keys_to_delete = [key for key in self._tasks if str(key).startswith(task_id)]
        

        if not keys_to_delete:
            raise TaskNotFoundError(task_id)
        
        if len(keys_to_delete) > 1:
            raise ValueError(f"Ambiguous ID '{task_id}': {len(keys_to_delete)} tasks match this prefix.")
        
        target_key = keys_to_delete[0]
        deleted_task: Task = self._tasks.pop(target_key)
        self._save()
        return deleted_task
            
          
    
    # List Tasks
    def list_tasks(self) -> list[Task]:
        tasks_list = list(self._tasks.values())
        tasks_list.sort(key=lambda t: (t.created_at, t.task_id), reverse=True)
        return tasks_list
    

    
    # Task Saving Locally (Serialization)
    def _save(self) -> None:
        """
        Converting Task Objects into Json Strings
        """
        json_tasks = TypeAdapter(dict[UUID, Task]).dump_json(self._tasks, indent=4).decode()
        self._file_path.write_text(json_tasks, encoding='utf-8')

    # Task Retrival Locally (Deserialization)
    def _load(self) -> dict[UUID, Task]:
        """
        Converting Json Strings into Task Objects
        """
        validated_tasks = TypeAdapter(dict[UUID, Task]).validate_json(self._file_path.read_text(encoding='utf-8'))
        return validated_tasks
    

            
            
        