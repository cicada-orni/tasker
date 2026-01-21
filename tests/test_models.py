import uuid
from tasker import models

def test_init_values(task_shopping, task_laundry):
    assert isinstance(task_shopping.task_id,uuid.UUID)
    assert task_shopping.status == models.Status.Todo
    assert task_shopping.due_date is None
    assert task_shopping.created_at.tzinfo is not None
    assert task_shopping.tags == []
    
    assert task_laundry.priority == models.Priority.Medium
    assert task_laundry.due_date is None
    assert task_laundry.updated_at.tzinfo is not None

    assert task_laundry.tags is not task_shopping.tags
    assert task_laundry.task_id != task_shopping.task_id
    task_laundry.tags.append("urgent")
    assert task_laundry.tags != task_shopping.tags




    