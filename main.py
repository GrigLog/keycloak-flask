import flask
import requests

from urllib.parse import urlencode
import base64
import json

import urls
import utils
import constants

app = flask.Flask(__name__)
app.secret_key = constants.appSecretKey


@app.route('/')
def protectedResource():
    userInfo = None
    if ((token := flask.session.get('token')) is not None) and ((userInfo := utils.tryGetUserInfo(token)) is not None):
        return "Hello, {}!".format(userInfo['preferred_username'])
    authParams = {'response_type': 'code',
                  'client_id': constants.clientId,
                  'redirect_uri': urls.local+'auth',
                  'response_mode': 'jwt',
                  'scope': 'openid'}
    return flask.redirect(urls.authEndpoint + "?" + urlencode(authParams))


@app.route('/auth')
def auth():
    response = flask.request.args.get('response')
    print(flask.request.args)
    header, body = [json.loads(base64.b64decode(utils.addPaddingB64(e)).decode('utf-8')) for e in response.split('.')[:2]]
    print('HEADER:', header)
    print('BODY:', body)

    tokenParams = {
        'grant_type': 'authorization_code',
        'code': body['code'],
        'client_id': constants.clientId,
        'redirect_uri': urls.local+'auth',  # just for validation, KC will not redirect to the same address another time
        'client_secret': constants.clientSecret  # only required when client access type is "confidential"
    }
    r = requests.post(urls.tokenEndpoint, data=tokenParams).json()
    print(r)
    if 'error' in r:
        print(r)
        return "Unable to get access token."
    access_token = r['access_token']
    print(access_token)
    header, body = [json.loads(base64.b64decode(utils.addPaddingB64(e)).decode('utf-8')) for e in access_token.split('.')[:2]]
    print('HEADER:', header)
    print('BODY:', body)
    flask.session['token'] = access_token
    r = utils.tryGetUserInfo(access_token)
    if r is None:
        return "Unable to fetch user info."
    return flask.redirect('/')


@app.route('/logout')
def logout():
    return flask.redirect(urls.logoutEndpoint + "?" + urlencode({'redirect_uri': urls.local+'logged_out'}))


@app.route('/logged_out')
def loggedOut():
    return 'Logged out.'


app.run(port=5000)
