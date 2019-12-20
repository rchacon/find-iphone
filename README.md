# find-iphone

Script to "play sound" on your lost iPhone.

## Installation

```
python setup.py install
```

## Usage

```
find-iphone --help
```

### List My Devices

```
$ find-iphone -u hankhill@example.com get
Password:
[ {"id": "foo", "rawDeviceModel": "MacBookAir4,2", "deviceDisplayName": "MacBook Air 13\"", "name": "Hank\u2019s MacBook Air"},
  {"id": "bar", "rawDeviceModel": "iPhone9,2", "deviceDisplayName": "iPhone 7 Plus", "name": "iPhone"}]
 ```

### Play Sound

Play sound on my iPhone with Device ID: `bar`.

```
$ find-iphone -u hankhill@example.com play bar
```
