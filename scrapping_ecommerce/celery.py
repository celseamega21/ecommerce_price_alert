import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapping_ecommerce.settings")
app = Celery("scrapping_ecommerce")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
    "check-price-every-6-hours": {
        "task": "product.tasks.check_price",
        "schedule": crontab(minute=0, hour="*/12"),
    },
}