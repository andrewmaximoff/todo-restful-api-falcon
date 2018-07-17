# TODO: If task field doesn't exist raise exception AttributeError
# TODO: All raise overwrite on return error with appropriate code
import falcon

from collections import OrderedDict

from todoapi.models import Task


TASK_FIELDS = OrderedDict([
    ('id', lambda x: str(x.id)),
    ('owner', lambda x: str(x.owner)),
    ('title', lambda x: str(x.title)),
    ('timestamp', lambda x: str(x.timestamp)),
    ('done', lambda x: str(x.done)),
    ('tags', lambda x: x.tags),
])


class TaskResource:

    def on_get(self, req, resp, task_id=None):
        user = req.context.get('user')
        if task_id is not None:
            tasks = Task.objects(id=task_id).all()
            total_tasks = tasks.count()
        else:
            tasks = Task.objects(owner=user).all()
            total_tasks = tasks.count()

        if total_tasks <= 0:
            error = 'No tasks remaining.'
            tasks = []
        else:
            error = None
            tasks = self._prepare_task(tasks)

        resp.json = {
            'data': {
                'tasks': tasks,
                'total': total_tasks,
            },
            'error': error is not None,
            'msg': error or 'Task(s) successfully retrieved.'
        }

        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, task_id=None):
        if task_id is not None:
            raise falcon.HTTPUnauthorized(
                title='409 Conflict',
                description='You can\'t create task by specifying the ID',
                challenges=None)

        user = req.context.get('user')

        task = Task(
            owner=user,
            title=req.get_json('title'),
            body=req.get_json('body'),
            tags=req.get_json('tags')
        )

        task.save()
        task_fields = self._prepare_task([task])

        error = None

        resp.json = {
            'error': error is not None,
            'msg': error or 'Task created!',
            'data': {
                'task': task_fields
            }
        }

        resp.status = falcon.HTTP_201

    def on_put(self, req, resp, task_id=None):
        if task_id is None:
            raise falcon.HTTPUnauthorized(
                title='409 Conflict',
                description='Task by current id doesn\'t exists!',
                challenges=None)

        task = Task.objects(id=task_id).first()
        task.update(
            title=req.get_json('title', default=None),
            body=req.get_json('body', default=None),
            tags=req.get_json('tags', default=None)
        )
        task.reload()

        task_fields = self._prepare_task([task])

        error = None

        resp.json = {
            'data': {
                'task': task_fields
            },
            'error': error is not None,
            'msg': error or 'Task updated!',
        }

        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, task_id=None):
        if task_id is None:
            raise falcon.HTTPUnauthorized(
                title='409 Conflict',
                description='You didn\'t specify a task id!',
                challenges=None)
        task = Task.objects(id=task_id).first()
        if not task:
            raise falcon.HTTPUnauthorized(
                title='409 Conflict',
                description='Task by current id doesn\'t exists!',
                challenges=None)
        task_fields = self._prepare_task([task])
        task.delete()

        error = None

        resp.json = {
            'data': {
                'task': task_fields
            },
            'error': error is not None,
            'msg': error or 'Task deleted!',
        }

        resp.status = falcon.HTTP_200

    @staticmethod
    def _prepare_task(tasks):
        return [
            {
                k: v(task) for k, v in TASK_FIELDS.items()
            } for task in tasks
        ]
