import os

from celery.result import AsyncResult
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app.api.v1.schemas.response import DetailedTask
from app.services import ServiceMixin


class TasksCeleryService(ServiceMixin):
    @staticmethod
    async def download_report_by_task_result(report_name: str) -> FileResponse:
        reports_dir = f"reports/{report_name}"

        if os.path.exists(reports_dir):
            headers = {
                "Content-Disposition": f'attachment; filename="{report_name}"'
            }
            return FileResponse(
                path=reports_dir,
                headers=headers,
                filename=report_name,
                media_type="application/"
                "vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet",
            )
        else:
            raise HTTPException(
                status_code=404, detail="menu report not found"
            )

    @staticmethod
    def get_task_result(task_id: str):
        task = AsyncResult(task_id)

        if task.successful():
            return DetailedTask(
                task_id=task.task_id,
                status=task.status,
                result=task.result,
            )

        return DetailedTask(task_id=task.task_id, status=task.status)
