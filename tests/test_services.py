import pytest
from tasker.exceptions import TaskValidationError
from tasker.models import Status, Priority


def test_empty_tasks_list(task_service):
    # initial list is empty
    assert len(task_service.list_tasks()) == 0
    
    
def test_create_task_and_ordering(task_service):
    # create multiple tasks
    task_service.create_task(title='Cleaning', description='Clean the house', status=Status.In_Progress, priority=Priority.High)
    task_service.create_task(title='Going out', description='Going out for dinner')
    # tasks lists are populated
    all_tasks = task_service.list_tasks()
    assert len(all_tasks) == 2
    assert all_tasks[0].created_at >= all_tasks[1].created_at

def test_tasks_validation(task_service):
    # raise TaskValidationError
    with pytest.raises(TaskValidationError):
        task_service.create_task()
    with pytest.raises(TaskValidationError) as excinfo:
        task_service.create_task(title='task_1', random_key=234)
    assert 'not permitted' in str(excinfo.value)
    assert 'random_key' in str(excinfo.value)

def test_enums_normalization(task_service):
    task_study = task_service.create_task(title='study', status='IN-PROGRESS', priority='HIGH')
    assert task_study.status == Status.In_Progress
    assert task_study.priority == Priority.High

def test_enums_validation(task_service):
    with pytest.raises(TaskValidationError):
        task_service.create_task(title='test_task', priority='urgent')



    

    