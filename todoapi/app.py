import falcon
import mongoengine

from todoapi.serialize import error_serializer
from todoapi.middleware import (
    jsonify,
    auth,
)
from todoapi.route import routes

try:
    import settings_local as settings
except ImportError:
    import settings


class ToDo(falcon.API):
    def __init__(self):
        super(ToDo, self).__init__(
            middleware=[
                jsonify.JsonifyMiddleware(),
                auth.BasicAuthMiddleware(
                    exempt_routes=[
                        '/api/v0.1/auth',
                        '/api/status'
                    ]
                )
            ]
        )
        mongoengine.connect(
            settings.MONGO['DATABASE'],
            host=settings.MONGO['HOST'],
            port=settings.MONGO['PORT'],
            username=settings.MONGO['USERNAME'],
            password=settings.MONGO['PASSWORD']
        )

        self.settings = settings
        self.set_error_serializer(error_serializer.serialize_to_json)
        # Build routes
        for (uri_template, resource_cls) in routes.items():
            resource = resource_cls()
            self.add_route(uri_template, resource)

    def start(self):
        """ A hook to when a Gunicorn worker calls run()."""
        pass

    def stop(self, signal):
        """ A hook to when a Gunicorn worker starts shutting down. """
        pass
