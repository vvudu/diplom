from celery import shared_task
from easy_thumbnails.files import generate_all_aliases
from backend.models import User, Product, Shop, Category, ProductInfo, Parameter, ProductParameter
from django.core.mail import send_mail
from django.conf import settings
import requests
from yaml import safe_load
import os
import logging

logger = logging.getLogger(__name__)

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
def do_import(source):
    """Фоновый импорт данных из YAML-файла (локальный путь или URL)"""
    try:
        if source.startswith(('http://', 'https://')):
            response = requests.get(source)
            response.raise_for_status()
            data = safe_load(response.content)
        else:
            with open(source, 'r', encoding='utf-8') as file:
                data = safe_load(file)

        shop, _ = Shop.objects.get_or_create(name=data['shop'])

        for category_data in data['categories']:
            category, _ = Category.objects.get_or_create(
                id=category_data['id'],
                defaults={'name': category_data['name']}
            )
            category.shops.add(shop)

        ProductInfo.objects.filter(shop=shop).delete()

        for item in data['goods']:
            product, _ = Product.objects.get_or_create(
                name=item['name'],
                category_id=item['category']
            )

            product_info = ProductInfo.objects.create(
                product=product,
                shop=shop,
                external_id=item['id'],
                model=item['model'],
                price=item['price'],
                price_rrc=item['price_rrc'],
                quantity=item['quantity']
            )

            for param_name, param_value in item['parameters'].items():
                parameter, _ = Parameter.objects.get_or_create(name=param_name)
                ProductParameter.objects.create(
                    product_info=product_info,
                    parameter=parameter,
                    value=param_value
                )

        return f"Data imported successfully from {source}"

    except Exception as e:
        logger.error(f"Failed to import data from {source}: {e}")
        return f"Error importing data from {source}: {e}"


@shared_task
def generate_thumbnails(instance_id, model_name):
    """Асинхронная генерация миниатюр изображений"""
    instance = None
    if model_name == 'User':
        instance = User.objects.get(id=instance_id)
        if instance.avatar:
            generate_all_aliases(instance.avatar, include_global=True)

    elif model_name == 'Product':
        instance = Product.objects.get(id=instance_id)
        if instance.image:
            generate_all_aliases(instance.image, include_global=True)

    return f"Thumbnails generated for {model_name} {instance_id}"
