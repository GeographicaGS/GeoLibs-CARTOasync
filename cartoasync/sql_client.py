import aiohttp

from .exceptions import CartoException


class SQLClient():

    def __init__(self, auth, session=None):
        self.__auth = auth
        self.__session = session
        self.__external_session = True if session is not None else False

    async def close(self):
        await self.__session.close()

    async def send(self, query, format='json'):
        kwargs = {
            'params': {
                'api_key': self.__auth.api_key,
                'format': format
            },
            'data': {
                'q': query
            },
            'ssl': self.__auth.ssl
        }

        if self.__external_session:
            async with self.__session.post(self.__auth.sql_api_url, **kwargs) as resp:
                return await self.handle_response(resp, format)

        else:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.__auth.sql_api_url, **kwargs) as resp:
                    return await self.handle_response(resp, format)

    async def handle_response(self, resp, format):
        if resp.status != 200:
            return await self.handle_error(resp)

        elif format in ['json', 'geojson']:
            return await resp.json()

        else:
            return await resp.read()

    async def handle_error(self, resp):
        url = f'{resp.method} {resp.url.scheme}://{resp.url.host}{resp.url.path}'

        if resp.status == 400:
            data = await resp.json()
            exc = CartoException(data)

        elif resp.status == 401:
            exc = CartoException(f'Unauthorized - No authentication provided - {url}')

        elif resp.status == 404:
            exc = CartoException(f'Not found - {url}')

        elif resp.status == 403:
            exc = CartoException(f'Forbidden - The API key does not authorize this request - {url}')

        elif resp.status == 429:
            exc = CartoException(f"You are over platform's limits - {url}")

        else:
            exc = CartoException(f'Error {resp.status} - {url}')

        exc.status = resp.status
        raise exc
