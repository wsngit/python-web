# server.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse

# Создаем экземпляр приложения FastAPI
app = FastAPI(title="Simple HTTP API", version="0.1.0")

# 1. Эхо-запрос (возвращает полученное сообщение в текстовой форме)
@app.get("/echo/{message}", response_class=PlainTextResponse)
async def echo_message(message: str):
    """Возвращает полученное сообщение обратно."""
    return f"Эхо: {message}"

# 2. GET-запрос, который возвращает информацию о запросе в JSON
@app.get("/request-info")
async def get_request_info(request: Request):
    """Возвращает метод, заголовки и параметры запроса."""
    return {
        "method": request.method,
        "headers": dict(request.headers),
        "query_params": dict(request.query_params)
    }

# 3. POST-запрос, который возвращает информацию о запросе и теле запроса
@app.post("/request-info")
async def post_request_info(request: Request):
    """Возвращает метод, заголовки и тело POST-запроса."""
    # Пытаемся получить тело запроса в формате JSON
    try:
        body = await request.json()
    except:
        body = "Не удалось распарсить JSON"

    return {
        "method": request.method,
        "headers": dict(request.headers),
        "body": body
    }

# 4. PUT-запрос, который возвращает информацию о запросе и теле запроса
@app.put("/request-info")
async def put_request_info(request: Request):
    """Возвращает метод, заголовки и тело PUT-запроса."""
    try:
        body = await request.json()
    except:
        body = "Не удалось распарсить JSON"

    return {
        "method": request.method,
        "headers": dict(request.headers),
        "body": body
    }

# 5. POST-запрос для сложения двух чисел
@app.post("/sum")
async def calculate_sum(request: Request):
    """Получает два числа и возвращает их сумму."""
    try:
        # Пытаемся получить JSON из тела запроса
        data = await request.json()
        a = data["a"]
        b = data["b"]

        # Проверяем, что это числа
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("a и b должны быть числами")

        return {"result": a + b}

    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except:
        raise HTTPException(status_code=400, detail="Неверный формат данных")

# Эндпоинт для проверки работоспособности сервера
@app.get("/")
async def root():
    return {"message": "Сервер работает! Доступные эндпоинты: /echo/{message}, /request-info, /sum"}

