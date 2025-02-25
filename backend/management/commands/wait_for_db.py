from django.core.management.base import BaseCommand
import time
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Команда для ожидания доступности базы данных перед запуском сервера"""
    
    def handle(self, *args, **options):
        self.stdout.write("⏳ Ожидание базы данных...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write("⚠️  База данных недоступна, повторная попытка через 1 сек...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("✅ База данных доступна!"))
