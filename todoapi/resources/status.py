# TODO: create uri for check server status

class StatusResource:
    """
    REST API handlets for test
    """

    def on_get(self, req, resp):
        resp.json = {
            'msg': 'OK'
        }
