from config_data.config import load_config
import aiohttp

# Возвращает JSON ответ с названием, CIDом и свойствами, а так же status_code
async def get_properties(nametype, name) -> str:
    # Получение url для обращения к API
    api = load_config().api
    # Асинхронное обращение к API
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{api.url}:{api.port}/properties/{nametype}/{name}"
        ) as response:
            return await response.json(encoding="Windows-1252"), response.status