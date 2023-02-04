from celery.result import AsyncResult

from app.api.v1.schemas.response import DetailedTask
from app.services import ServiceMixin


class TasksCeleryService(ServiceMixin):
    @staticmethod
    def get_task(task_id: str):
        task = AsyncResult(task_id)

        if task.successful():
            return DetailedTask(
                task_id=task.task_id, status=task.status, result=task.result
            )

        return DetailedTask(task_id=task.task_id, status=task.status)
