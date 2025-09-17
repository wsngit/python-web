import httpx
import asyncio

# Синхронный запрос
def sync_request():
    response = httpx.get('https://httpbin.org/json')
    print(f"Sync status: {response.status_code}")
    return response

# Асинхронный запрос
async def async_request():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://httpbin.org/json')
        print(f"Async status: {response.text}")
        return response

# Запуск
if __name__ == "__main__":
    # Синхронный вызов
    sync_response = sync_request()

    # Асинхронный вызов
    async_response = asyncio.run(async_request())
