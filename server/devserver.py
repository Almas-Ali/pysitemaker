import http.server
import socketserver
import os
from typing import Tuple


def server(PORT=7536, HOST='127.0.0.1', DEBUG=True):
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        # os.chdir('templates')
        print(f'serving at port http://{HOST}:{PORT}')
        httpd.serve_forever()


def StaticServer(PORT=7536, HOST='127.0.0.1', DEBUG=True, templates_dir='templates', static_dir='static'):
    Handler = Path
    os.chdir('templates')
    try:
        with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
            print(f'serving at port http://{HOST}:{PORT}')
            httpd.serve_forever()
            httpd.close_request()
    except OSError:
        print('[Errno 98] Address already in use !')

class Path(http.server.SimpleHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer, directory=None) -> None:
        super().__init__(request, client_address, server, directory=directory)

    def do_GET(self):
        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        # self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        # self.end_headers()

        # Extract query param
        # name = 'World'
        # query_components = parse_qs(urlparse(self.path).query)
        # if 'name' in query_components:
        #     name = query_components["name"][0]

        # Some custom HTML code, possibly generated by another function
        # html = f"<html><head></head><body><h1>Hello {name}!</h1></body></html>"

        # Writing the HTML contents with UTF-8
        # self.wfile.write(bytes(html, "utf8"))

        for name, value in self.URLPATTERNS.items():
            for url, template in value.items():
                if self.path == url:
                    self.path = os.path.join(self.TEMPLATES_DIR, template)
                    print('\n\n\n\n'+ self.TEMPLATES_DIR, template, url)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def urls(self, url: str, template: str):
        self.do_GET(self)

    def paths(self, urlpatterns, templates_dir):
        self.URLPATTERNS = urlpatterns
        self.TEMPLATES_DIR = templates_dir


class Static():
    def __init__(self, static_dir):
        self.static_dir = static_dir

    def url_for(self, static_path: str):
        if_file = os.path.isfile(os.path.join(self.static_dir, static_path))
        is_exists = os.path.exists(os.path.join(self.static_dir, static_path))

        return os.path.abspath(static_path)


# # Create an object of the above class
# handler_object = Path

# PORT = 8000
# my_server = socketserver.TCPServer(("", PORT), handler_object)

# # Star the server
# my_server.serve_forever()
