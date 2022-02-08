import flask
import requests
import urls


def addPaddingB64(s: str):
    s += '=' * ((4 - len(s)) % 4)
    return s


def tryGetUserInfo(token: str):
    r = requests.post(urls.userInfoEndpoint, headers={'Authorization': 'Bearer ' + token}).json()
    if 'error' in r:
        print(r)
        return None
    return r
