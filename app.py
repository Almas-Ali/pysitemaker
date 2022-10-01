# make pysitemaker app

from pysitemaker import PySiteMaker


app = PySiteMaker('My Site')

# set static and template directories

app.set_static_dir('static')

app.set_template_dir('templates')

# set routes


@app.router.route('/')
def index(request):
    return app.template_env.get_template('index.html').render()


@app.router.route('/about')
def about(request):
    return app.template_env.get_template('about.html').render()


@app.router.route('/contact')
def contact(request):
    return app.template_env.get_template('contact.html').render()


@app.router.route('/blog')
def blog(request):
    return app.template_env.get_template('blog.html').render()


app.run(HOST='127.0.0.1', PORT=7536, DEBUG=True)
