import falcon
import mongoengine
from todoapi.middleware import jsonify
from todoapi.routes import routes

try:
    import settings_local as settings
except ImportError:
    import settings


class ToDo(falcon.API):
    def __init__(self):
        super(ToDo, self).__init__(
            middleware=[
                jsonify.Middleware()
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
