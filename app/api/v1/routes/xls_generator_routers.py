from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse

from app.api.v1.docs.menu_methods_description import ReportGenerators
from app.api.v1.schemas import response as res_model
from app.celery.tasks import create_report_xlsx
from app.services.service import Services, service_stub

xlsx_generator_router = APIRouter(prefix="/report")


@xlsx_generator_router.post(
    "/xlsx",
    tags=["Report generators"],
    description=ReportGenerators.POST_XLSX,
    summary=ReportGenerators.POST_XLSX,
    status_code=status.HTTP_202_ACCEPTED,
    response_model=res_model.CreatedTask,
)
async def create_task_for_generate_xlsx(
    services: Services = Depends(service_stub),
):
    """
    Create task in celery for generating a .xlsx file of menu

    :param services: Services for application
    :return: created task id
    """
    menus = await services.report_generator_service.get_all_data()
    task = create_report_xlsx.apply_async(args=[menus])

    return res_model.CreatedTask(task_id=task.id)


@xlsx_generator_router.get(
    "/xlsx/{task_id}",
    tags=["Report generators"],
    description=ReportGenerators.GET_XLSX,
    summary=ReportGenerators.GET_XLSX,
    response_model=res_model.DetailedTask,
)
async def get_status_of_task_xlsx(
    task_id: str, services: Services = Depends(service_stub)
):
    """
    Get detailed info about task

    :param services: Services for application
    :param task_id: target task id
    :return: detailed info about task
    """
    task = services.tasks_service.get_task_result(task_id)

    return task


@xlsx_generator_router.get(
    "/xlsx/download/f/{file_name}",
    tags=["Report generators"],
    description=ReportGenerators.DOWNLOAD_XLSX,
    summary=ReportGenerators.DOWNLOAD_XLSX,
    responses={status.HTTP_404_NOT_FOUND: {"detail": "menu report not found"}},
    response_class=FileResponse,
)
async def download_xlsx_report_if_exists(
    file_name: str, services: Services = Depends(service_stub)
) -> FileResponse:
    """
    Download from reports folder report by name file_name if exists

    :param file_name: name of report
    :param services: Services for application
    :return: FileResponse or NotFound
    """
    return await services.tasks_service.download_report_by_task_result(
        file_name
    )
