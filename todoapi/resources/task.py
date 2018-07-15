import falcon

from todoapi.models import User, Task


class TaskResource:

    def on_get(self, req, resp):
        user = req.context.get('user')

        tasks = Task.objects(owner=user)
        total_tasks = tasks.count()

        if total_tasks < 0:
            error = 'No tasks remaining.'
            tasks = []
        else:
            error = None
            tasks = self._prepare_task(tasks)

        data = {
            'tasks': tasks,
            'total': total_tasks,
            'error': error is not None,
            'msg': error or 'Task(s) successfully retrieved.'
        }

        resp.json = data
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        user = req.context.get('user')
        task = Task(
            owner = req.get_json('owner'),
            title = req.get_json('title'),
            body = req.get_json('body'),
            timestamp = req.get_json('timestamp'),
            done = req.get_json('done'),
            tags = req.get_json('tags'),
        )

    @staticmethod
    def _prepare_task(tasks):
        return [
            {
                'owner': str(task.owner),
                'title': str(task.title),
                'body': str(task.body),
                'timestamp': str(task.timestamp),
                'done': str(task.done),
                'tags': str(task.tags),
            } for task in tasks
        ]
