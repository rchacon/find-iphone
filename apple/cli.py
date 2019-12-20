"""
CLI for apple module
"""
import argparse
import getpass
import pprint

from . import __version__, auth
from .devices import DeviceClient


def get(args):
    creds = auth.AppleAuth()
    creds.signin(args.username, args.password)

    client = DeviceClient(creds)
    data = client.get()

    pprint.pprint(data, indent=2)


def play(args):
    creds = auth.AppleAuth()
    creds.signin(args.username, args.password)

    client = DeviceClient(creds)
    data = client.playsound(args.device)

    pprint.pprint(data, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__ + '(v %s)' % __version__)
    parser.add_argument('-u', '--username', required=True, help='Apple ID')
    parser.add_argument('-p', '--password', help='iCloud password')

    subparsers = parser.add_subparsers(description='command')

    get_parser = subparsers.add_parser('get', description='Get my devices')
    get_parser.set_defaults(func=get)

    find_parser = subparsers.add_parser('play', description='Find my iPhone')
    find_parser.add_argument('device', help='iPhone Device ID')
    find_parser.set_defaults(func=play)

    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass('Password: ')

    args.func(args)


if __name__ == '__main__':
    main()
