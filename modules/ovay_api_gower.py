import aiohttp
from dotenv import load_dotenv

from inits.logger import db_logger

load_dotenv()


class ApiClient:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    async def get(self, endpoint):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}{endpoint}",
                                   headers=self.headers) as response:
                if response.status != 200:
                    db_logger.debug(
                        f"Error:Ошибка GET запроса к endpoint: "
                        f"{endpoint}:Вернулся статус код: "
                        f"{response.status}")
                    return None
                db_logger.debug(f'Успешно отправлен GET[{response.status}] '
                                f'запрос в БД к эндпоину {endpoint}')

                return await response.json()

    async def post(self, endpoint, data):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}{endpoint}", json=data,
                                    headers=self.headers) as response:
                if response.status != 201:
                    db_logger.debug(
                        f"Error:Ошибка POST запроса к endpoint {endpoint}"
                        f":Вернулся статус код: "
                        f"{response.status}")
                    return None
                db_logger.debug(f'Успешно отправлен POST[{response.status}] '
                                f'запрос в БД к эндпоину {endpoint}')
                return await response.json()

    async def patch(self, endpoint, data, pk):
        async with aiohttp.ClientSession() as session:
            async with session.patch(f"{self.url}{endpoint}{pk}/", json=data,
                                     headers=self.headers) as response:
                if response.status != 200:
                    db_logger.debug(
                        f"Error:Ошибка PATCH запроса к endpoint"
                        f" {endpoint}:Вернулся статус код: "
                        f"{response.status}")
                    return None
                db_logger.debug(f'Успешно отправлен PATCH[{response.status}] '
                                f'запрос в БД к эндпоину {endpoint}')
                return await response.json()

    async def put(self, endpoint, data, pk):
        async with aiohttp.ClientSession() as session:
            async with session.put(f"{self.url}{endpoint}{pk}/", json=data,
                                   headers=self.headers) as response:
                if response.status != 200:
                    db_logger.debug(
                        f"Error:Ошибка PUT запроса к endpoint"
                        f" {endpoint}:Вернулся статус код: "
                        f"{response.status}")
                    return None
                db_logger.debug(f'Успешно отправлен PUT[{response.status}] '
                                f'запрос в БД к эндпоину {endpoint}')
                return await response.json()

    async def delete(self, endpoint, pk):
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self.url}{endpoint}{pk}/",
                                      headers=self.headers) as response:
                if response.status != 204:
                    db_logger.debug(
                        f"Error:Ошибка DELETE запроса к endpoint"
                        f" {endpoint}:Вернулся статус код: "
                        f"{response.status}")
                    return None
                db_logger.debug(f'Успешно отправлен DELETE[{response.status}] '
                                f'запрос в БД к эндпоину {endpoint}')
                return {'status': 'deleted'}



