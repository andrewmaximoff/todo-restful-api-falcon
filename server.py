from wsgiref import simple_server
from todoapi.app import ToDo
import os


if __name__ == '__main__':
    api = ToDo()
    httpd = simple_server.make_server(os.getenv('SERVER_BIND', '127.0.0.1'), 8000, api)
    httpd.serve_forever()
