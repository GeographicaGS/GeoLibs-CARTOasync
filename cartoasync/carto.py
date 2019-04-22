import aiohttp


class CartoException(Exception):
    pass


class Auth():

    CLOUD_URL_TEMPLATE = 'https://{username}.carto.com'
    USER_URL_INFIX = '/user/{username}'
    SQL_API_URL_SUFFIX = '/api/v2/sql'

    def __init__(self, base_url=None, username=None, api_key=None, ssl=None):
        if not base_url and not username:
            raise CartoException('base_url or username must be provided')

        self.__base_url_param = base_url
        self.__username = username
        self.api_key = api_key
        self.ssl = ssl

        self.__base_url = None
        self.__url_path = ''
        self.sql_api_url = ''

        self.__create_base_url()
        self.__create_sql_api_url()

    def __create_base_url(self):
        if not self.__base_url_param:  # CARTO cloud w/o organization
            self.__base_url = self.CLOUD_URL_TEMPLATE.format(username=self.__username)
            return

        # Delete slash if it exists for the next two cases
        if self.__base_url_param[-1] == '/':
            self.__base_url_param = self.__base_url_param[:-1]

        if not self.__username:  # CARTO cloud w/ organization or CARTO OnPremises for implict users
            self.__base_url = self.__base_url_param
            self.__username = self.__base_url_param.split('/')[-1]
            return

        # CARTO cloud w/ organization or CARTO OnPremises for explicit users
        self.__base_url = self.__base_url_param
        self.__url_path = self.USER_URL_INFIX.format(username=self.__username)
        return

    def __create_sql_api_url(self):
        self.sql_api_url = self.__base_url + self.__url_path + self.SQL_API_URL_SUFFIX


class SQLClient():

    def __init__(self, auth):
        self.__auth = auth
        self.__session = aiohttp.ClientSession()

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

        async with self.__session.post(self.__auth.sql_api_url, **kwargs) as resp:
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
