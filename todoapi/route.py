from todoapi.resources import (
    status,
    auth,
    task
)


routes = {
    '/api/status': status.StatusResource,
    '/api/v0.1/auth': auth.AuthResource,
    '/api/v0.1/task': task.TaskResource,
    '/api/v0.1/task/{task_id}': task.TaskResource,
}
