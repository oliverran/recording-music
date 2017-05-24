from flask import render_template, Blueprint, request, send_from_directory
from flask.views import MethodView
from ..model import db, Human, Studio, News
import os

music = Blueprint('music', __name__, static_folder='', static_url_path='')

UPLOAD_FOLDER = os.getcwd() + r'/app/static/uploads'


@music.route('/index/')
def index():
    return render_template('index_music.html')


@music.route('/profile/<filename>/')
def render_img(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@music.route('/profile/<filename>/')
def render_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


class MusicHuman(MethodView):
    def get(self, page=1):
        itmes = Human.query.paginate(page, per_page=8)  # 博客列表、分页
        return render_template('music_human.html', music_humans=itmes)


class RecordingStudio(MethodView):
    def get(self, page=1):
        itmes = Studio.query.paginate(page, per_page=8)  # 博客列表、分页
        return render_template('recording_studio.html', studios=itmes)


class NewsView(MethodView):
    def get(self, page=1):
        itmes = News.query.paginate(page, per_page=8)  # 博客列表、分页
        return render_template('news.html', news=itmes)


@music.route('/about-us/')
def about_us():
    return render_template('about_us.html')


# @music.route('/page/<int:id>/')
# def music_human_page(id=None):
#     item = db.session.query(Human).get(id)
#     return render_template('three.html')

class MusicHumanPage(MethodView):
    def get(self, id=None):
        item = db.session.query(Human).get(id)
        return render_template('music_human_page.html', item=item)


class RecordingStudioPage(MethodView):
    def get(self, id=None):
        item = db.session.query(Studio).get(id)
        return render_template('recording_studio_page.html', item=item)


class NewsPage(MethodView):
    def get(self, id=None):
        item = db.session.query(News).get(id)
        return render_template('news_page.html', item=item)
