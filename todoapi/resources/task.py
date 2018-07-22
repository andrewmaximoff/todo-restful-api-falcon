from collections import OrderedDict

import falcon
import mongoengine

from todoapi.models import Task


TASK_FIELDS = OrderedDict([
    ('id', lambda x: str(x.id)),
    ('owner', lambda x: str(x.owner.username)),
    ('title', lambda x: str(x.title)),
    ('body', lambda x: str(x.body)),
    ('timestamp', lambda x: str(x.timestamp)),
    ('done', lambda x: str(x.done)),
    ('tags', lambda x: x.tags),
])


class TaskResource:

    def on_get(self, req, resp, task_id=None):
        user = req.context.get('user')
        if task_id is None:
            tasks = Task.objects(owner=user).all()
            total_tasks = tasks.count()
        else:
            try:
                tasks = Task.objects(id=task_id).all()
                total_tasks = tasks.count()
            except mongoengine.ValidationError:
                raise falcon.HTTPBadRequest(
                    title='400 Bad Request',
                    description='Invalid task id!'
                )
            if not tasks:
                raise falcon.HTTPBadRequest(
                    title='400 Bad Request',
                    description='Task by current id doesn\'t exists!'
                )

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
            raise falcon.HTTPBadRequest(
                title='400 Bad Request',
                description='To create a task you don\'t need to specify id.'
            )

        user = req.context.get('user')

        task = Task(
            owner=user,
            title=req.get_json('title'),
            body=req.get_json('body', default=None),
            tags=req.get_json('tags', default=None),
            done=req.get_json('done', default=None)
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
            raise falcon.HTTPBadRequest(
                title='400 Bad Request',
                description='You didn\'t specify task id!'
            )
        try:
            task = Task.objects(id=task_id).first()
        except mongoengine.ValidationError:
            raise falcon.HTTPBadRequest(
                title='400 Bad Request',
                description='Invalid task id!'
            )

        if task is None:
            raise falcon.HTTPBadRequest(
                title='400 Bad Request',
                description='Task by current id doesn\'t exists!'
            )

        task.modify(
            title=req.get_json('title', default=None),
            body=req.get_json('body', default=None),
            tags=req.get_json('tags', default=None),
            done=req.get_json('done', default=None)
        )

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

    def on_delete(self, req, resp):
        tasks = req.get_json('tasks', default=None)
        if tasks is None:
            raise falcon.HTTPBadRequest(
                title='400 Bad Request',
                description='You didn\'t specify a task id(s)!'
            )
        try:
            tasks = Task.objects(id__in=tasks).all()
        except mongoengine.ValidationError:
            raise falcon.HTTPBadRequest(
                title='400 Bad Request',
                description='Invalid task id(s)!'
            )

        if not tasks:
            raise falcon.HTTPBadRequest(
                title='400 Bad Request',
                description='Task by current id(s) doesn\'t exists!'
            )
        tasks.delete()

        error = None

        resp.json = {
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
