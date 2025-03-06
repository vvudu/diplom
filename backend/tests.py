from django.test import TestCase
from django.urls import reverse
from backend.models import User, Shop, Category, Product

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@example.com', password='TestPass123')

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, 'test@example.com')

class ShopModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email='shop@example.com', password='TestPass123')
        cls.shop = Shop.objects.create(name="Test Shop", user=user)

    def test_shop_str(self):
        self.assertEqual(str(self.shop), "Test Shop")

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Electronics")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Books")
        cls.product = Product.objects.create(name="Django Guide", category=category)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Django Guide")

class RegisterAccountViewTest(TestCase):
    def test_register_user_success(self):
        url = reverse('backend:user-register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'ComplexPass123!',
            'company': 'CompanyX',
            'position': 'Developer'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], True)
        self.assertTrue(User.objects.filter(email='john@example.com').exists())

    def test_register_user_missing_fields(self):
        url = reverse('backend:user-register')
        data = {
            'email': 'john@example.com',
            'password': 'ComplexPass123!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], False)
