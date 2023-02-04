from celery import Celery

from app.config.cfg import load_config


def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        _, queue = name.split(":")
        return {"queue": queue}

    return {"queue": "celery"}


celery = Celery(
    __name__,
    include=["app.celery.tasks"],
)
celery.config_from_object(load_config().celery)
celery.conf.task_default_queue = "celery"
celery.conf.task_routes = (route_task,)
celery.autodiscover_tasks()
