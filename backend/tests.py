from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from backend.models import User, Shop, Category, Product, ProductInfo, Contact, Order, OrderItem


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
        data = {'email': 'john@example.com', 'password': 'ComplexPass123!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Status'], False)


class LoginAccountViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='login@example.com', password='LoginPass123', is_active=True)

    def test_login_success(self):
        url = reverse('backend:user-login')
        response = self.client.post(url, {'email': 'login@example.com', 'password': 'LoginPass123'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['Status'])
        self.assertIn('Token', response.json())


class BasketViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='basket@example.com', password='BasketPass123', is_active=True)
        self.token, _ = Token.objects.get_or_create(user=self.user)

        category = Category.objects.create(name='Tech')
        shop = Shop.objects.create(name='Shop 1', state=True)
        product = Product.objects.create(name='Laptop', category=category)
        self.product_info = ProductInfo.objects.create(
            product=product, shop=shop, external_id=1, quantity=5, price=1000, price_rrc=1200
        )

    def auth_headers(self):
        return {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

    def test_add_to_basket(self):
        url = reverse('backend:basket')
        data = {'items': f'[{{"product_info": {self.product_info.id}, "quantity": 1}}]'}
        response = self.client.post(url, data, **self.auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['Status'])

    def test_get_basket(self):
        Order.objects.create(user=self.user, state='basket')
        url = reverse('backend:basket')
        response = self.client.get(url, **self.auth_headers())
        self.assertEqual(response.status_code, 200)


class ContactViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='contact@example.com', password='ContactPass123', is_active=True)
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def auth_headers(self):
        return {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

    def test_create_contact(self):
        url = reverse('backend:user-contact')
        data = {'city': 'CityX', 'street': 'StreetY', 'phone': '123456789'}
        response = self.client.post(url, data, **self.auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['Status'])
        self.assertEqual(Contact.objects.count(), 1)
