"""
Module for accessing info about your Apple devices.
"""
from http import HTTPStatus
import json

import requests
from requests.cookies import cookiejar_from_dict

from . import AppleError
from . import settings


class Device:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.device_display_name = data['deviceDisplayName']
        self.raw_device_model = data['rawDeviceModel']

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'deviceDisplayName': self.device_display_name,
            'rawDeviceModel': self.raw_device_model
        })


class DeviceClient:
    def __init__(self, credentials):
        self.credentials = credentials
        self.session = requests.Session()
        self.session.headers.update({'Origin': settings.ICLOUD_URL})
        self.session.cookies = cookiejar_from_dict(credentials.cookies)

    def get(self):
        opts = {
            'params': self.credentials.build_details,
            'timeout': settings.HTTP_TIMEOUT
        }
        resp = self.session.post(settings.CLIENT_URL, **opts)

        data = resp.json()

        devices = []
        for item in data['content']:
            devices.append(Device(item))

        return devices

    def playsound(self, device_id):
        opts = {
            'params': self.credentials.build_details,
            'json': {
                'device': device_id,
                'subject': 'Find My iPhone Alert'
            },
            'timeout': settings.HTTP_TIMEOUT
        }
        resp = self.session.post(settings.PLAYSOUND_URL, **opts)

        if resp.status_code != HTTPStatus.OK:
            raise AppleError(resp.status_code)

        return resp.json()
