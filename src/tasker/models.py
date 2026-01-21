# Task domain model will live here
from enum import StrEnum, auto
import uuid
from datetime import datetime, UTC
from pydantic import BaseModel, Field, ConfigDict




# Status Enums
class Status(StrEnum):
    Todo = auto()
    In_Progress = auto()
    Done = auto()

# Priority Enums
class Priority(StrEnum):
    Low = auto()
    Medium = auto()
    High = auto()



# Task Class
class Task(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='forbid')

    task_id: uuid.UUID = Field(default_factory=uuid.uuid4, frozen=True)
    title: str = Field(min_length=1)
    description: str = "" 
    status: Status = Status.Todo
    priority: Priority = Priority.Medium
    due_date: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    tags: list[str] = Field(default_factory=list)

    

    

    


    
