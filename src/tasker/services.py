from tasker.storage import Storage
from tasker.models import Task
from tasker.exceptions import TaskValidationError
from pydantic import ValidationError
from uuid import UUID
from typing import TypedDict, Unpack, cast
from tasker.models import Status, Priority
from datetime import datetime


# Task Create Schema
class TaskCreateArgs(TypedDict, total=False):
    title: str
    description: str
    status: Status | str
    priority: Priority | str
    due_date: datetime | None
    tags: list[str]


class TaskService:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage
    # ENUM Normalization
    def _normalize_enum_input(self, enum_value: str) -> str:
        splitted_enum = enum_value.replace("-", " ").split()
        clean_enum_value = "_".join(splitted_enum).lower()
        return clean_enum_value
    
    # CREATE LOGIC
    def create_task(self, **task_data: Unpack[TaskCreateArgs]) -> Task:
        """
        Pydantic will fill in 'status' and 'description' automatically.
        Example: TaskService.create_task(title="Buy Milk")
        """
        if "status" in task_data and isinstance(task_data["status"], str):
            # normalization/cleaning enums
            clean_status = self._normalize_enum_input(task_data["status"])
            try:
                # converting to actual enum
                task_data["status"] = cast(Status, Status(clean_status))
            except ValueError:
                raise TaskValidationError(
                    f"{task_data['status']} is not a valid status"
                )

        if "priority" in task_data and isinstance(task_data["priority"], str):
            clean_priority = self._normalize_enum_input(task_data["priority"])
            try:
                task_data["priority"] = cast(Priority, Priority(clean_priority))
            except ValueError:
                raise TaskValidationError(
                    f"{task_data['priority']} is not a valid priority."
                )
            
        if 'tags' in task_data and isinstance(task_data['tags'], str):
            cleaned_tags = [tag.strip() for tag in task_data['tags'].split(',')]
            try:
                task_data['tags'] = cleaned_tags
            except ValidationError as e:
                raise TaskValidationError(e) from e

        try:
            new_task = Task(**task_data)  # type: ignore
            self.storage.add_task(new_task)
            return new_task

        except ValidationError as e:
            raise TaskValidationError(e) from e

    # READ LOGIC
    def get_task(self, task_id: UUID) -> Task:
        return self.storage.get_task(task_id)
    
    def delete_task(self, task_id: str) -> Task:
        return self.storage.delete_task(task_id)
        
        

    # LIST LOGIC
    def list_tasks(self) -> list[Task]:
        return self.storage.list_tasks()
    

