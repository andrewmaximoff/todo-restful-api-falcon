from mongoengine.connection import get_db


class Resource:
    """
    REST API handlets for test
    """

    def on_get(self, req, resp):
        db = get_db()
        resp.json = {
            'msg': 'OK',
            'db_dir': str(dir(db)),
            'db_name': db.name,

        }
