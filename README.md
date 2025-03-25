## 📌 Документация по развёртыванию и настройке проекта Django REST API

---

### 🚀 1. Описание проекта

Проект представляет собой RESTful API интернет-магазина на базе Django и Django Rest Framework, поддерживает асинхронные задачи через Celery и Redis, хранение данных в PostgreSQL и мониторинг производительности с помощью Django Silk. Реализована авторизация через Google OAuth2 и автоматизировано тестирование с покрытием через GitHub Actions.

---

### 🛠️ 2. Структура проекта

```text
netology_pd_diplom/
├── backend/                 # Основное приложение проекта
├── netology_pd_diplom/      # Настройки Django проекта
├── tests/                   # Тесты проекта
├── manage.py                # Консоль Django
├── requirements.txt         # Зависимости проекта
├── Dockerfile               # Docker-конфигурация
├── docker-compose.yml       # Docker-compose конфигурация
└── .github/workflows/       # GitHub Actions для CI и покрытия кода
```

---

### 📦 3. Требования к окружению

- Python 3.12
- Docker и Docker Compose

---

### 💻 4. Локальное развёртывание

#### 4.1 Клонирование репозитория

```bash
git clone https://github.com/vvudu/diplom.git
cd diplom
```

#### 4.2 Запуск Docker Compose

```bash
docker compose up -d --build
```

Будут запущены:
- Django-приложение (`localhost:8000`)
- PostgreSQL (`localhost:5432`)
- Redis (`localhost:6379`)
- Celery worker и Celery beat

---

### ⚙️ 5. Применение миграций и создание суперпользователя

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

---

### 🔧 6. Настройка OAuth2 авторизации Google

1. Создать OAuth-приложение в [Google Cloud Console](https://console.cloud.google.com/).
2. Получить `Client ID` и `Client Secret`.
3. Настроить `settings.py`:

```python
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '<Google Client ID>'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '<Google Client Secret>'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/'
```

4. Выполнить миграции:

```bash
docker compose exec web python manage.py migrate
```

Проверка авторизации доступна по ссылке:
```
http://localhost:8000/auth/login/google-oauth2/
```

---

### 📊 7. Django Silk (профилирование)

Интерфейс Silk доступен по ссылке:
```
http://localhost:8000/silk/
```

---

### 🧪 8. Запуск тестов и покрытие кода

```bash
docker compose exec web coverage run manage.py test
docker compose exec web coverage report
```

Подробный отчёт (HTML):
```bash
docker compose exec web coverage html
```

---

### ⚙️ 9. GitHub Actions

Настроен автоматический запуск тестов и расчёт покрытия при создании Pull Request.

Конфигурация в файле:
```
.github/workflows/python-coverage.yml
```

---

### 🐳 10. Полезные Docker-команды

- Проверка контейнеров:
```bash
docker compose ps
```
- Остановка контейнеров:
```bash
docker compose down
```
- Логи:
```bash
docker compose logs web
```

---

Теперь проект готов к использованию и дальнейшему развитию!
