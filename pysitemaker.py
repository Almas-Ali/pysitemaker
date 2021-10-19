import http.server
import socketserver
import os
from typing import Tuple


class PySiteMaker:
    '''Python Based Website Maker.'''

    def __init__(self, site_name):
        self.site_name = site_name

    def dir_config(self, templates_dir='templates', static_dir='static'):
        self.templates_dir = templates_dir
        self.static_dir = static_dir

    def static_url(self, static_path: str):
        is_file = os.path.isfile(
            os.path.join(self.static_dir, static_path))
        is_exists = os.path.exists(
            os.path.join(self.static_dir, static_path))
        if is_file:
            return os.path.abspath(static_path)
        else:
            return is_exists

    class Path(http.server.SimpleHTTPRequestHandler):

        def paths(self, urlpatterns: dict, templates_dir: str):
            self.urlpatterns = urlpatterns
            self.templates_dir = templates_dir
            print(self.urlpatterns, self.templates_dir)

        def do_GET(self):
            self.send_response(200)
            for url, template in self.urlpatterns.items():
                if self.path == url:
                    self.path = os.path.join(self.templates_dir, template)
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        # def urls(self, url: str, template: str):
        #     self.do_GET(self)

    @staticmethod
    def run(HOST='127.0.0.1', PORT=7536, DEBUG=True):
        Handler = PySiteMaker.Path
        os.chdir('templates')
        try:
            with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
                print(f'serving at port http://{HOST}:{PORT}')
                httpd.serve_forever()
        except OSError:
            print('[Errno 98] Address already in use !')
