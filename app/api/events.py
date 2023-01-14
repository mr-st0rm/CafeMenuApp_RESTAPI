import logging

from fastapi import APIRouter

event_handler = APIRouter()


@event_handler.on_event("startup")
async def application_started():
    logging.info("App started.")


@event_handler.on_event("shutdown")
async def application_exit():
    logging.info("App shutdown.")
