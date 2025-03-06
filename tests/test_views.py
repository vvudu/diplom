import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from backend.models import Product, Order, Category, Shop, ProductInfo, OrderItem, Contact

# Фикстура для API-клиента
@pytest.fixture
def client():
    return APIClient()

# Фикстура для тестового пользователя
@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",  # Добавляем email, так как он обязателен
        password="testpass",
        type="buyer"
    )

# Фикстура для создания тестового магазина
@pytest.fixture
def shop(db, user):
    return Shop.objects.create(name="Test Shop", user=user)

# Фикстура для создания категории (если у Product есть ForeignKey на Category)
@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")

# Фикстура для создания тестового продукта
@pytest.fixture
def product(db, category):
    return Product.objects.create(name="Test Product", category=category)

# Фикстура для создания информации о продукте
@pytest.fixture
def product_info(db, product, shop):
    return ProductInfo.objects.create(
        product=product,
        shop=shop,
        external_id=12345,
        quantity=10,
        price=100,
        price_rrc=120
    )

# Фикстура для создания контакта пользователя
@pytest.fixture
def contact(db, user):
    return Contact.objects.create(
        user=user,
        city="Test City",
        street="Test Street",
        house="1",
        phone="1234567890"
    )

# Фикстура для создания тестового заказа
@pytest.fixture
def order(db, user, contact):
    return Order.objects.create(user=user, state="new", contact=contact)

# Фикстура для создания заказанного товара
@pytest.fixture
def order_item(db, order, product_info):
    return OrderItem.objects.create(order=order, product_info=product_info, quantity=2)

# Тест: получение списка заказов (авторизованный пользователь)
@pytest.mark.django_db
def test_order_list_authenticated(client, user):
    client.force_authenticate(user=user)
    url = reverse("order-list")  # Убедись, что этот маршрут есть в urls.py
    response = client.get(url)
    assert response.status_code == 200

# Тест: получение деталей заказа
@pytest.mark.django_db
def test_order_detail_authenticated(client, user, order):
    client.force_authenticate(user=user)
    url = reverse("order-detail", args=[order.id])
    response = client.get(url)
    assert response.status_code == 200

# Тест: создание заказа (авторизованный пользователь)
@pytest.mark.django_db
def test_create_order_authenticated(client, user, product_info):
    client.force_authenticate(user=user)
    url = reverse("order-list")
    data = {
        "products": [{"id": product_info.id, "quantity": 1}]
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 201

# Тест: создание заказа неавторизованным пользователем (должен вернуть 403 Forbidden)
@pytest.mark.django_db
def test_create_order_unauthenticated(client, product_info):
    url = reverse("order-list")
    data = {
        "products": [{"id": product_info.id, "quantity": 1}]
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 403

# Тест: создание заказа с некорректными данными (несуществующий продукт)
@pytest.mark.django_db
def test_create_order_invalid_data(client, user):
    client.force_authenticate(user=user)
    url = reverse("order-list")
    data = {
        "products": [{"id": 99999, "quantity": 1}]
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 400

# Тест: получение списка продуктов
@pytest.mark.django_db
def test_product_list(client):
    url = reverse("product-list")  # Убедись, что этот маршрут есть
    response = client.get(url)
    assert response.status_code == 200

# Тест: получение деталей продукта
@pytest.mark.django_db
def test_product_detail(client, product):
    url = reverse("product-detail", args=[product.id])
    response = client.get(url)
    assert response.status_code == 200

# Тест: создание продукта (требует авторизации)
@pytest.mark.django_db
def test_create_product_authenticated(client, user, category):
    client.force_authenticate(user=user)
    url = reverse("product-list")
    data = {
        "name": "New Product",
        "category": category.id
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 201

# Тест: создание продукта неавторизованным пользователем (403 Forbidden)
@pytest.mark.django_db
def test_create_product_unauthenticated(client, category):
    url = reverse("product-list")
    data = {
        "name": "New Product",
        "category": category.id
    }
    response = client.post(url, data, format="json")
    assert response.status_code == 403
