from constants import realm

keycloakHost = 'http://localhost:8080'
baseUrl = '{}/auth/realms/{}/protocol/openid-connect/'.format(keycloakHost, realm)

authEndpoint = baseUrl + "auth"
tokenEndpoint = baseUrl + "token"
logoutEndpoint = baseUrl + "logout"
local = 'http://localhost:5000/'
