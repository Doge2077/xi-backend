import requests
from apps.app01 import settings


def login(code):
    response = requests.get(settings.code2Session.format(settings.AppId, settings.AppSecret, code))
    data = response.json()
    print(data)
    if data.get("openid"):
        return data
    else:
        return False
