from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, \
    Contact, ConfirmEmailToken
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html
from celery.result import AsyncResult
from backend.tasks import do_import  # Импорт Celery-задачи

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Панель управления пользователями
    """
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password', 'type')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'company', 'position')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


#@admin.register(Shop)
#class ShopAdmin(admin.ModelAdmin):
#    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at',)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """Админ-панель для магазинов с кнопкой запуска импорта"""
    
    change_list_template = "admin/import_changelist.html"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import/', self.admin_site.admin_view(self.start_import), name='start-import'),
        ]
        return custom_urls + urls

    def start_import(self, request):
        """ Функция для запуска Celery-задачи из админки """
        result = do_import.delay("http://127.0.0.1:8001/shop1.yaml")  # Запуск задачи Celery
        self.message_user(request, f"Импорт запущен! ID задачи: {result.id}")
        return HttpResponseRedirect("../")

    def import_button(self, obj):
        return format_html('<a class="button" href="import/">Запустить импорт</a>')
    
    import_button.short_description = "Импорт товаров"
    import_button.allow_tags = True