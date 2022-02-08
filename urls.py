keycloakHost = 'http://localhost:8080'
realm = 'newrealm'
clientId = 'myclient'
baseUrl = '{}/auth/realms/{}/protocol/openid-connect/'.format(keycloakHost, realm)

authEndpoint = baseUrl + "auth"
tokenEndpoint = baseUrl + "token"
userInfoEndpoint = baseUrl + "userinfo"
logoutEndpoint = baseUrl + "logout"
local = 'http://localhost:5000/'
