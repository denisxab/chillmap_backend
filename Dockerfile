# Используйте официальный образ Python
FROM python:3.11

# Установка рабочей директории
WORKDIR /app

# Копирование файла зависимостей в рабочую директорию
COPY pyproject.toml poetry.lock ./

RUN apt install -y make

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Установка зависимостей с использованием Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копирование остальных файлов приложения в рабочую директорию
COPY . .

# Установка переменной среды, чтобы вывод не буферизовался
ENV PYTHONUNBUFFERED=1

# Запуск команды по умолчанию
CMD python manage.py migrate && \ 
    make css_to_drf && \
    make loaddata && \
    python manage.py runserver 0.0.0.0:8181
