from wsgiref import simple_server
from todoapi.app import ToDo
import os


if __name__ == '__main__':
    port = 8000
    host = os.getenv('SERVER_BIND', '127.0.0.1')
    api = ToDo()
    print("======== Running on http://{}/{} ========\n"
          "(Press CTRL+C to quit)".format(host, port))
    httpd = simple_server.make_server(os.getenv('SERVER_BIND', host), port, api)
    httpd.serve_forever()
