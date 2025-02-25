import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netology_pd_diplom.settings')

app = Celery('netology_pd_diplom')

# Загружает конфигурацию из Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит задачи
app.autodiscover_tasks()
