# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Установка и запуск PostgreSQL
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Команда для запуска Flask
CMD ["python", "app.py"]
