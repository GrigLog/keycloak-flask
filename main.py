import flask
import requests

from urllib.parse import urlencode

import urls
import utils
import constants
from time import time


app = flask.Flask(__name__)
app.secret_key = constants.appSecretKey


@app.route('/')
def protectedResource():
    token = flask.session.get('token')
    jwt = None
    if token is not None and (jwt := utils.parseJwt(token))['body']['exp'] > time():
        return "Hello, {}!".format(jwt['body']['preferred_username'])
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
    jwt = utils.parseJwt(response)
    print('HEADER:', jwt['header'])
    print('BODY:', jwt['body'])

    tokenParams = {
        'grant_type': 'authorization_code',
        'code': jwt['body']['code'],
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
    jwt = utils.parseJwt(access_token)
    print('HEADER:', jwt['header'])
    print('BODY:', jwt['body'])
    flask.session['token'] = access_token
    return flask.redirect('/')


@app.route('/logout')
def logout():
    flask.session['token'] = None
    return flask.redirect(urls.logoutEndpoint + "?" + urlencode({'redirect_uri': urls.local+'logged_out'}))


@app.route('/logged_out')
def loggedOut():
    return 'Logged out.<br><a href = http://localhost:5000>Main page</a>'


app.run(port=5000)
