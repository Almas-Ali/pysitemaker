# pysitemaker class with web server and template engines complex querys


from urllib.parse import urlparse, parse_qs
import socket
import threading
import json
from jinja2 import Environment, FileSystemLoader


class PySiteMaker:
    def __init__(self, site_name):
        self.site_name = site_name
        self.router = Router()
        self.host = None
        self.port = None
        self.debug = False
        self.static_dir = None
        self.template_dir = None
        self.template_env = None
        self.server = None

    def run(self, HOST, PORT, DEBUG):
        self.host = HOST
        self.port = PORT
        self.debug = DEBUG
        self.server = Server(self.host, self.port, self.debug, self.router)
        self.server.run()

    def set_static_dir(self, static_dir):
        self.static_dir = static_dir

    def set_template_dir(self, template_dir):
        self.template_dir = template_dir
        self.template_env = Environment(
            loader=FileSystemLoader(self.template_dir))


class Router:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def wrapper(func):
            self.routes[path] = func
            return func
        return wrapper

    def get_route(self, path):
        return self.routes.get(path)


class Server:
    def __init__(self, host, port, debug, router):
        self.host = host
        self.port = port
        self.debug = debug
        self.router = router
        self.server = None

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Server started at {self.host}:{self.port}...")

        while True:
            client, address = self.server.accept()
            print(f"Client connected from {address}")
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        request = client.recv(1024).decode()
        if not request:
            return

        request = Request(request)
        response = Response()
        route = self.router.get_route(request.path)
        if route:
            response.body = route(request)
        else:
            response.body = f"Route {request.path} not found!"

        client.sendall(response.get_response())
        client.close()


class Request:
    def __init__(self, request):
        request = request.splitlines()
        self.method, self.path, self.protocol = request[0].split(" ")
        self.headers = {}
        self.query = {}
        self.body = {}

        for line in request[1:]:
            if not line:
                break
            key, value = line.split(": ")
            self.headers[key] = value

        if self.method == "GET":
            self.query = parse_qs(urlparse(self.path).query)
        elif self.method == "POST":
            self.body = json.loads(request[-1])


class Response:
    def __init__(self):
        self.status = 200
        self.headers = {}
        self.body = ""

    def get_response(self):
        response = f"HTTP/1.1 {self.status} OK"

        for key, value in self.headers.items():
            response += f"\r{key}: {value}"

        response += f"\r\n\r\n{self.body}"
        return response.encode()
