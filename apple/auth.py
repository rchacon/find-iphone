"""
Handle iCloud Auth
"""
from http import HTTPStatus
from json import JSONDecodeError
from urllib.parse import parse_qs, urlparse

from lxml.html import document_fromstring
import requests

from . import AppleError
from . import settings


class AppleAuth:
    def __init__(self):
        self.session = requests.Session()
        self.cookies = None
        self._widget_key = None
        self._build_details = None

    @property
    def build_details(self):
        if self._build_details:
            return self._build_details

        self._build_details = self.get_build_details()

        return self._build_details

    @property
    def widget_key(self):
        if self._widget_key:
            return self._widget_key

        self._widget_key = self.get_widget_key()

        return self._widget_key

    def get_build_details(self):
        opts = {
            'timeout': settings.HTTP_TIMEOUT
        }
        resp = self.session.get(settings.FIND_URL, **opts)

        if resp.status_code != HTTPStatus.OK:
            raise AppleError(resp.status_code)

        root = document_fromstring(resp.text)

        return {
            'clientBuildNumber': root.get('data-cw-private-build-number'),
            'clientMasteringNumber': root.get('data-cw-private-mastering-number')
        }

    def get_widget_key(self):
        opts = {
            'params': self.build_details,
            'timeout': settings.HTTP_TIMEOUT
        }
        resp = self.session.get(settings.VALIDATE_URL, **opts)

        try:
            url = resp.json()['configBag']['urls']['accountLoginUI']
        except JSONDecodeError:
            raise AppleError('Could not decode JSON from %s', resp.request.url)
        except KeyError:
            raise AppleError('Unexpected response from %s', resp.request.url)

        return parse_qs(urlparse(url).query)['widgetKey'][0]

    def set_cookies(self, session_token):
        opts = {
            'headers': {'Origin': settings.ICLOUD_URL},
            'params': self.build_details,
            'json': {
                'dsWebAuthToken': session_token,
                'accountCountryCode': 'USA',  # TODO: be global
                'extended_login': False
            },
            'timeout': settings.HTTP_TIMEOUT
        }
        resp = self.session.post(settings.ACCOUNT_LOGIN_URL, **opts)

        self.cookies = dict(resp.cookies)

    def signin(self, username, password):
        opts = {
            'headers': {'X-Apple-Widget-Key': self.widget_key},
            'json': {
                'accountName': username,
                'password': password,
                'rememberMe': False,
                'trustTokens': []
            },
            'timeout': settings.HTTP_TIMEOUT
        }
        resp = self.session.post(settings.SIGNIN_URL, **opts)

        self.set_cookies(resp.headers['X-Apple-Session-Token'])
