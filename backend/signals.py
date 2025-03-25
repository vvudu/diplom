from typing import Type

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created
from backend.tasks import generate_thumbnails
from backend.models import ConfirmEmailToken, User, Product

new_user_registered = Signal()
new_order = Signal()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """Отправляем письмо с токеном для сброса пароля"""
    msg = EmailMultiAlternatives(
        f"Password Reset Token for {reset_password_token.user}",
        reset_password_token.key,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )
    msg.send()


@receiver(post_save, sender=User)
def new_user_registered_signal(sender: Type[User], instance: User, created: bool, **kwargs):
    """Отправляем письмо с подтверждением почты, и запускаем генерацию миниатюры аватара пользователя"""
    if created and not instance.is_active:
        token, _ = ConfirmEmailToken.objects.get_or_create(user_id=instance.pk)
        msg = EmailMultiAlternatives(
            f"Email Confirmation Token for {instance.email}",
            token.key,
            settings.EMAIL_HOST_USER,
            [instance.email]
        )
        msg.send()
        
    # Запуск генерации миниатюр аватара при наличии аватара у пользователя
    if instance.avatar:
        generate_thumbnails.delay(instance.id, 'User')


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """Отправляем письмо при изменении статуса заказа"""
    user = User.objects.get(id=user_id)
    msg = EmailMultiAlternatives(
        "Обновление статуса заказа",
        'Заказ сформирован',
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    msg.send()


@receiver(post_save, sender=Product)
def product_image_thumbnail(sender: Type[Product], instance: Product, created: bool, **kwargs):
    """Асинхронная генерация миниатюр изображений товара после его создания или обновления"""
    if instance.image:
        generate_thumbnails.delay(instance.id, 'Product')
