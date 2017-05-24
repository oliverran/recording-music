from flask import Flask, render_template, redirect, url_for
from app.music import music
from app.admin import admin
from app.admin.view import login_manager
from .model import db


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprint(app)
    # register_errorhandlers(app)

    @app.route('/', methods=['GET'])
    def hello():
        return redirect(url_for('music.index'))

    return app


def register_blueprint(app):
    app.register_blueprint(music)
    app.register_blueprint(admin, url_prefix='/admin')


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_errorhandlers(app):
    def render_error(e):
        return render_template('error_page/%s.html' % e.code), e.code

    for e in [401, 404, 500]:
        app.errorhandler(e)(render_error)
