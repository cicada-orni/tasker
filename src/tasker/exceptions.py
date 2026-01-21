from uuid import UUID
from pydantic import ValidationError


class TaskNotFoundError(Exception):
    def __init__(self, task_id: UUID):
        self.task_id = task_id
        err_msg = f"Task with ID {task_id} not found in storage."
        super().__init__(err_msg)

class TaskAlreadyExistsError(Exception):
    def __init__(self, task_id: UUID):
        self.task_id = task_id
        err_msg = f"Task with id {task_id} already exists."
        super().__init__(err_msg)

class TaskValidationError(Exception):
    def __init__(self, error: ValidationError | str):
        if isinstance(error, ValidationError):
            self.errors = [f"{err['loc'][0]}: {err['msg']}" for err in error.errors()]
            self.message = f"Validation failed: {' | '.join(self.errors)}"
        else:
            self.message = error
            
            
        super().__init__(self.message)
