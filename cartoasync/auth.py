from .exceptions import CartoException


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
