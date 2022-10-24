from celery import Celery

from core.config import get_settings

settings = get_settings()

REDIS_URL = "redis://{0}:{1}/0".format(settings.redis.host, settings.redis.port)

celery_app = Celery(__name__)
# celery_app.autodiscover_tasks(["users.tasks"])

celery_app.conf.broker_url = REDIS_URL
celery_app.conf.result_backend = REDIS_URL
celery_app.conf.accept_content = ["json"]
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
