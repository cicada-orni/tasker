from abc import ABC, abstractmethod
from tasker.models import Task
from uuid import UUID
from tasker.exceptions import TaskNotFoundError, TaskAlreadyExistsError

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


class TaskStorage(Storage):
    def __init__(self) -> None:
        self._tasks: dict[UUID, Task] = {}

    def add_task(self, task: Task) -> None:
        if task.task_id in self._tasks:
            raise TaskAlreadyExistsError(task.task_id)
        self._tasks[task.task_id] = task

    def get_task(self, task_id: UUID) -> Task:
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        return self._tasks[task_id]
    
    def list_tasks(self) -> list[Task]:
        tasks_list = list(self._tasks.values())
        tasks_list.sort(key=lambda t: (t.created_at, t.task_id), reverse=True)
        return tasks_list


