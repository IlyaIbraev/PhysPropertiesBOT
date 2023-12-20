import requests
from config_data.config import load_config

# Возвращает JSON ответ с названием, CIDом и свойствами, а так же status_code
def get_properties(nametype, name) -> str:
    # Получение url для обращения к API
    api = load_config().api
    response = requests.get(
        f"{api.url}:{api.port}/properties/{nametype}/{name}"
    )
    return response.json(), response.status_code