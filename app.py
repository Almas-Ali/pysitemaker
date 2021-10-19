# from pysitemaker.server.devserver import StaticServer
# from server.devserver import StaticServer
# from server.devserver import Path, Static
from pysitemaker import PySiteMaker
from jinja2 import Environment, FileSystemLoader

app = PySiteMaker(__file__)

# Directory settings
TEMPLATE_DIR = 'templates'
STATIC_DIR = 'test'

# Host settings
HOST = "127.0.0.1"
PORT = 7536

app.dir_config(templates_dir=TEMPLATE_DIR, static_dir=STATIC_DIR)
# static = app.Static(static_dir=STATIC_DIR)
# path = Path

# print(static.url_for('test.py'))

# urlpatterns = [
#     path.urls(url='/', template='index.html'),
# ]

URLPATTERNS = {
    # "/url" : "template.html",
    "/index": "index.html",
}

app.Path.paths(app, urlpatterns=URLPATTERNS, templates_dir=TEMPLATE_DIR)

app.run(HOST=HOST, PORT=PORT, DEBUG=True)
