FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости и ставим их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . /app/

# Открываем порт 8000
EXPOSE 8000

# Запуск через стандартный Django runserver (для разработки)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
