from flask import Flask, jsonify
from authlib.integrations.flask_client import OAuth
from loginpass import create_flask_blueprint
from loginpass import OAUTH_BACKENDS

app = Flask(__name__)
app.config.from_pyfile('config.py')


oauth = OAuth(app)


@app.route('/')
def index():
    tpl = '<li><a href="/{}/login">{}</a></li>'
    lis = [tpl.format(b.NAME, b.NAME) for b in OAUTH_BACKENDS]
    return '<ul>{}</ul>'.format(''.join(lis))


def handle_authorize(remote, token, user_info):
    return jsonify(user_info)


for backend in OAUTH_BACKENDS:
    bp = create_flask_blueprint(backend, oauth, handle_authorize)
    app.register_blueprint(bp, url_prefix='/{}'.format(backend.NAME))
