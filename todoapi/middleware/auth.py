# TODO: Add exempt_methods in Auth
import base64

import falcon

from todoapi.models import User

class BasicAuthMiddleware:
    def __init__(self, exempt_routes=None):
        self.auth_header_prefix = 'Basic'
        self.exempt_routes = exempt_routes or []

    def process_resource(self, req, resp, resource, params):
        """
        Extract basic auth token from request `authorization` header,  deocode the
        token, verifies the username/password and return either a ``user``
        object if successful else raise an `falcon.HTTPUnauthoried exception`
        """
        if req.path not in self.exempt_routes:
            username, password = self._extract_credentials(req)
            user = self.user_loader(username, password)
            if not user:
                raise falcon.HTTPUnauthorized(
                    title='401 Unauthorized',
                    description='Invalid Username/Password',
                    challenges=None).to_json()
            req.context['user'] = user

    def user_loader(self, username, password):
        return True

    def _extract_credentials(self, req):
        auth = req.get_header('Authorization')

        if not auth:
            raise falcon.HTTPUnauthorized(
                title='401 Unauthorized',
                description='Missing Authorization Header',
                challenges=None)

        token = self._parse_auth_token_from_request(auth_header=auth)
        try:
            token = base64.b64decode(token).decode('utf-8')
        except Exception as ex:
            raise falcon.HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid Authorization Header: Unable to decode credentials',
                challenges=None)

        try:
            username, password = token.split(':')
        except ValueError:
            raise falcon.HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid Authorization: Unable to decode credentials',
                challenges=None)

        return username, password

    def _parse_auth_token_from_request(self, auth_header):
        """
        Parses and returns Auth token from the request header. Raises
        `falcon.HTTPUnauthoried exception` with proper error message
        """
        parts = auth_header.split()

        if parts[0].lower() != self.auth_header_prefix.lower():
            raise falcon.HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid Authorization Header: '
                            'Must start with {0}'.format(self.auth_header_prefix),
                challenges=None)

        elif len(parts) == 1:
            raise falcon.HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid Authorization Header: Token Missing',
                challenges=None)
        elif len(parts) > 2:
            raise falcon.HTTPUnauthorized(
                title='401 Unauthorized',
                description='Invalid Authorization Header: Contains extra content',
                challenges=None)

        return parts[1]
