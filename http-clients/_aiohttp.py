import aiohttp
import asyncio

async def async_request():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/json') as response:
            return await response.json()

# Запуск
if __name__ == "__main__":
    async_response = asyncio.run(async_request())
    print(async_response)