# ==================== Stage 1: Builder ====================
FROM python:3.12-slim AS builder

WORKDIR /app

# Создаем виртуальное окружение
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==================== Stage 2: Runtime ====================
FROM python:3.12-slim

# Устанавливаем runtime зависимости
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем виртуальное окружение из builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Создаем пользователя
RUN groupadd -r django && useradd -r -g django django

WORKDIR /app

# Копируем код приложения
COPY --chown=django:django ./django_security .

USER django

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "django_security.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]