from fastapi import APIRouter, Depends, Response, status

from app.api.v1.docs.menu_methods_description import FillDatabaseDocs
from app.services.service import Services, service_stub

db_fill_router = APIRouter()


@db_fill_router.post(
    "/fill_db",
    tags=["Fill Database"],
    description=FillDatabaseDocs.POST_FILL,
    summary=FillDatabaseDocs.POST_FILL,
    status_code=status.HTTP_201_CREATED,
)
async def fill_db(services: Services = Depends(service_stub)):
    """
    Fill database with any records

    :param services: Services for business logic
    """
    await services.db_service.fill_db()

    return Response(status_code=status.HTTP_201_CREATED)
