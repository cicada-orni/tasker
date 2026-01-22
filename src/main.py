from tasker.models import Task, Status, Priority
from tasker.storage import TaskStorage
from tasker.exceptions import TaskNotFoundError, TaskAlreadyExistsError
import uuid


if __name__ == "__main__":
    task_1 = Task(
        title="Laundry",
        description="Washing the clothes",
        tags=["urgent", "must be done today"],
        status=Status.In_Progress,
        priority=Priority.High,
    )

    storage = TaskStorage()
    storage.add_task(task_1)
    try:
        print(storage.get_task(task_1.task_id))
    except TaskNotFoundError as e:
        print(e)

    try:
        print(storage.get_task(uuid.uuid4()))
    except TaskNotFoundError as e:
        print(e)

    try:
        storage.add_task(task_1)
    except TaskAlreadyExistsError as e:
        print(e)
