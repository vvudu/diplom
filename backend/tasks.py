from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import time

@shared_task
def send_email(subject, message, recipient_list):
    """Фоновая отправка email"""
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )
    return f"Email sent to {recipient_list}"

@shared_task
def do_import(data):
    """Фоновый импорт данных (эмуляция работы)"""
    time.sleep(5)  # Имитация долгого процесса
    return f"Data {data} imported!"
