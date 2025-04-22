import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapping_ecommerce.settings")
app = Celery("scrapping_ecommerce")
app.conf.broker_connection_retry_on_startup = True
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_heartbeat = 60
app.conf.worker_heartbeat_interval = 60
app.autodiscover_tasks()
app.conf.beat_schedule = {
    "check-price-every-4-hours": {
        "task": "product.tasks.check_price",
        "schedule": crontab(minute=0, hour="*/4"),
    },
}
