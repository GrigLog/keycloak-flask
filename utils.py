import json
import base64


def addPaddingB64(s: str):
    s += '=' * ((4 - len(s)) % 4)
    return s


def parseJwt(token: str):
    header, body = [json.loads(base64.b64decode(addPaddingB64(e)).decode('utf-8')) for e in token.split('.')[:2]]
    return {'header': header, 'body': body, 'signature': token.split('.')[2]}
