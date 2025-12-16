# ==================== Stage 1: Django Static Builder ====================
FROM python:3.12-slim AS static-builder

# Устанавливаем системные зависимости для Django
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем requirements первыми для лучшего кэширования
COPY backend/requirements.txt .

# Устанавливаем зависимости Django
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код Django
COPY backend/ .

# Настраиваем переменные окружения для сборки
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=django_security.settings \
    STATIC_ROOT=/app/static-collected \
    DEBUG=False

WORKDIR /app/django_security

# Собираем статику Django
RUN mkdir -p /app/static-collected && python manage.py collectstatic --noinput --clear

# Проверяем, что статика собралась
RUN ls -la /tmp/static

# ==================== Stage 2: Production Nginx ====================
FROM nginx:1.24-alpine

# Устанавливаем дополнительные пакеты
RUN apk update && apk add --no-cache \
    curl \
    openssl \
    tzdata \
    && rm -rf /var/cache/apk/*

# Копируем статику Django из static-builder stage
COPY --from=static-builder /tmp/static /static

# Генерируем самоподписанный SSL сертификат
RUN mkdir -p /etc/nginx/ssl && openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key \
    -out /etc/nginx/ssl/nginx.crt \
    -subj "/C=RU/ST=Moscow/L=Moscow/O=Development/CN=localhost" \
    -addext "subjectAltName = DNS:localhost, DNS:*.localhost, IP:127.0.0.1"

# Создаем директории
RUN mkdir -p /usr/share/nginx/html/media /media /var/cache/nginx

# Копируем конфигурацию Nginx
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/conf.d/ /etc/nginx/conf.d/

# Создаем health check endpoint
RUN echo '{"status": "healthy", "service": "nginx", "static": "embedded"}' > /usr/share/nginx/html/health.json

# Настраиваем пользователя и права
RUN chown -R nginx:nginx /usr/share/nginx/html /static && \
    chmod -R 755 /usr/share/nginx/html /static

# Экспортируем порты
EXPOSE 80 443

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]