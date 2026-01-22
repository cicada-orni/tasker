from tasker.models import Task
from tasker.exceptions import TaskNotFoundError, TaskAlreadyExistsError
import pytest
import uuid


def test_storage(task_shopping, task_storage):
    task_storage.add_task(task_shopping)
    get_task = task_storage.get_task(task_shopping.task_id)
    assert isinstance(get_task, Task)
    assert task_shopping.task_id == get_task.task_id
    with pytest.raises(TaskAlreadyExistsError):
        task_storage.add_task(task_shopping)
    with pytest.raises(TaskNotFoundError):
        task_storage.get_task(uuid.uuid4())
