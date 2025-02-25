# Используем Python 3.12
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app


# Копируем все файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Открываем порт 8000
EXPOSE 8000

# Запуск приложения через gunicorn
CMD ["gunicorn", "netology_pd_diplom.wsgi:application", "--bind", "0.0.0.0:8000"]
