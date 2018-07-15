from todoapi.resources import (
    status,
    auth
)


routes = {
    '/api/status': status.Resource,
    '/api/v0.1/auth': auth.Resource,
}
