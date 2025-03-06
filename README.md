1. Описание проекта
Проект представляет собой RESTful API интернет-магазина на базе Django и DRF, поддерживает асинхронные задачи через Celery и Redis. В качестве базы данных используется PostgreSQL.

2. Структура проекта

netology_pd_diplom/
├── backend/                 # Основное приложение проекта
├── netology_pd_diplom/      # Настройки Django проекта
├── tests/                   # Тесты проекта
├── manage.py                # Консоль Django
├── requirements.txt         # Зависимости проекта
├── Dockerfile               # Docker-конфигурация
├── docker-compose.yml       # Docker-compose конфигурация
└── .github/workflows/       # GitHub Actions для CI/CD и покрытия кода

3. Требования к окружению

Python 3.12
Docker & Docker Compose

4. Локальное развёртывание

4.1. Клонируй репозиторий

git clone https://github.com/vvudu/diplom.git
cd diplom

4.2. Создай виртуальное окружение и активируй его

python3 -m venv venv
source venv/bin/activate

4.3. Установи зависимости

pip install -r requirements.txt

4.4. Запусти контейнеры (Docker Compose)

docker compose up -d --build
Будут подняты:

Django-приложение (localhost:8000)
PostgreSQL (localhost:5432)
Redis (localhost:6379)
Celery worker и Celery beat (для фоновых задач)

5. Настройка окружения и переменных
Создай файл .env в корне проекта и добавь туда настройки (пример):

SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST_USER=shop.netology@mail.ru
EMAIL_HOST_PASSWORD=your-email-password

DATABASE_URL=postgres://user:password@localhost:5432/mydatabase
REDIS_URL=redis://localhost:6379/0

Обрати внимание: эти переменные нужны для безопасной работы приложения.

6. Применение миграций и запуск

docker compose exec web python manage.py migrate

Создание суперпользователя:

docker compose exec web python manage.py createsuperuser

Проект доступен по адресу:
➡️ http://localhost:8000/api/v1/

7. Тестирование и покрытие
Запуск тестов с покрытием:

coverage run manage.py test
coverage report

8. Docker-команды

Просмотреть запущенные контейнеры:

docker compose ps

Остановить контейнеры:

docker compose down

Просмотреть логи:

docker compose logs web
docker compose logs celery

9. GitHub Actions и покрытие тестами
Настроен автоматический запуск тестов с покрытием при создании Pull Request в ветку main.
Отчёт о покрытии тестами отображается в комментариях Pull Request.

Workflow лежит в:
.github/workflows/python-coverage.yml
