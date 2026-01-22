import pytest
from tasker.models import Task
from tasker.storage import TaskStorage
from tasker.services import TaskService


@pytest.fixture
def task_shopping() -> Task:
    task_1 = Task(title="Shopping", description="Need to buy groceries from mall")
    return task_1


@pytest.fixture()
def task_laundry() -> Task:
    task_2 = Task(title="Laundry", description="Need to wash clothes")
    return task_2


@pytest.fixture
def task_storage() -> TaskStorage:
    return TaskStorage()


@pytest.fixture
def task_service() -> TaskService:
    storage = TaskStorage()
    return TaskService(storage)
