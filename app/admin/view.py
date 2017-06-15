from flask import request, redirect, render_template, url_for, flash, Blueprint, send_from_directory
from flask.views import MethodView
from flask_login import LoginManager, login_user, login_required
from app.model import Human, User, db, Studio, News, Image
from .form import UserLoginForm, HumanForm, StudioForm, NewsForm, UploadForm
import os
from werkzeug.utils import secure_filename
import config

admin = Blueprint('admin', __name__, static_url_path='', )

login_manager = LoginManager()
login_manager.session_protection = "strong"
# UPLOAD_FOLDER = os.getcwd() + r'/app/static/uploads'
UPLOAD_FOLDER = config.BASE_PATH + r'/app/static/uploads'


@login_manager.user_loader  # 使用user_loader装饰器的回调函数非常重要，他将决定 user 对象是否在登录状态
def user_loader(id):  # 这个id参数的值是在 login_user(user)中传入的 user 的 id 属性
    user = User.query.filter_by(id=id).first()
    return user


# 呈现特定目录下的资源
@admin.route('/profile/<filename>/')
def render_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


class LoginView(MethodView):
    """登录函数"""

    # decorators = [login_required]  # 相当于 @login_required 装饰圈
    def get(self):
        form = UserLoginForm()
        return render_template('admin/login.html', form=form)

    def post(self):
        form = UserLoginForm()
        if form.validate_on_submit():
            user = db.session.query(User).filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=False)
                return redirect(url_for('admin.select_category'))
            else:
                flash('用户名或密码错误！')
        return render_template('admin/login.html', form=form)


"""TODO 做单独图片上传的功能,以及所有图片展示的功能,
    每个图片一个url,供富文本插入图片调用"""


class Images_list(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self, page=1):
        img = Image.query.paginate(page, per_page=10)  # flask SQLAlchemy方法 paginate（page，per_page= ）
        return render_template('admin/img_list.html', img=img)


class DelImg(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self, id=None):
        image = db.session.query(Image).get(id)  # 如果有id 从数据库读取这个id项
        img_name = image.img
        os.remove(UPLOAD_FOLDER + '/' + img_name)
        if image:
            db.session.delete(image)  # 如果有这个项  删除此项
            db.session.commit()
        return redirect(url_for('admin.img_list'))


class UploadImages(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self):
        form = UploadForm()  # 请求表单项内容
        return render_template('admin/upload_img.html', form=form)

    def post(self):
        form = UploadForm()  # 请求表单项内容
        img = Image()
        if form.img.data:
            f = form.img.data
            is_existence = db.session.query(Image).filter_by(img=f.filename).first()
            if is_existence is None:
                img.img = f.filename
                f.save(os.path.join(UPLOAD_FOLDER, f.filename))
                db.session.add(img)  # 向数据库添加
                db.session.commit()
            else:
                flash('文件名已存在')
                return render_template('admin/upload_img.html', form=form)
        return redirect(url_for('admin.img_list'))


# 管理员界面选择要管理的界面
class SelectCategory(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self):
        return render_template('admin/select_category.html')


# 分页功能实现
class HumanList(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self, page=1):
        humans = Human.query.paginate(page, per_page=10)  # flask SQLAlchemy方法 paginate（page，per_page= ）
        return render_template('admin/humans_list.html', humans=humans)


# 删除功能实现
class DelHuman(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self, id=None):
        if id:
            human = db.session.query(Human).get(id)  # 如果有id 从数据库读取这个id项
            if human:
                db.session.delete(human)  # 如果有这个项  删除此项
                db.session.commit()
        return redirect(url_for('admin.humans_list'))


# 文章创建编辑
class HumanCreateOrEdit(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self, id=None):
        human = Human() if not id else db.session.query(Human).get(id)  # 如果没有id创建实例，如果有数据库读取这个id项
        form = HumanForm(request.form) if not id else HumanForm(obj=human)  # 如果没有id 请求表单项内容，如果有表单内容是从数据库得到
        # form.log_category_id.choices = [(d.id, d.category) for d in Log_Category.query.all()]  # 分类从数据库查询到 做推导
        return render_template('admin/write-article.html', form=form)

    def post(self, id=None):
        form = HumanForm()  # 请求表单项内容
        human = Human() if not id else db.session.query(Human).get(id)  # 如果没有id创建实例，如果有数据库读取这个id项
        human.name = form.name.data
        human.content = form.content.data
        if form.img.data:
            human.img = form.img.data.filename
            f = form.img.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
        if not id:
            db.session.add(human)  # 向数据库添加
            db.session.commit()
        else:
            db.session.commit()
        return redirect(url_for('admin.humans_list'))


# 分页功能实现
class StudioList(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self, page=1):
        studios = Studio.query.paginate(page, per_page=10)  # flask SQLAlchemy方法 paginate（page，per_page= ）
        return render_template('admin/studios_list.html', studios=studios)


# 删除功能实现
class DelStudio(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self, id=None):
        if id:
            studio = db.session.query(Studio).get(id)  # 如果有id 从数据库读取这个id项
            if studio:
                db.session.delete(studio)  # 如果有这个项  删除此项
                db.session.commit()
        return redirect(url_for('admin.studio_list'))


# 文章创建编辑
class StudioCreateOrEdit(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self, id=None):
        studio = Studio() if not id else db.session.query(Studio).get(id)  # 如果没有id创建实例，如果有数据库读取这个id项
        form = StudioForm(request.form) if not id else StudioForm(obj=studio)  # 如果没有id 请求表单项内容，如果有表单内容是从数据库得到
        # form.log_category_id.choices = [(d.id, d.category) for d in Log_Category.query.all()]  # 分类从数据库查询到 做推导
        return render_template('admin/write-article.html', form=form)

    def post(self, id=None):
        form = StudioForm()  # 请求表单项内容
        studio = Studio() if not id else db.session.query(Studio).get(id)  # 如果没有id创建实例，如果有数据库读取这个id项
        studio.name = form.name.data
        studio.content = form.content.data
        if form.img.data:
            studio.img = form.img.data.filename
            f = form.img.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
        if not id:
            db.session.add(studio)  # 向数据库添加
            db.session.commit()
        else:
            db.session.commit()
        return redirect(url_for('admin.studio_list'))


class NewsList(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self, page=1):
        news = News.query.paginate(page, per_page=10)  # flask SQLAlchemy方法 paginate（page，per_page= ）
        return render_template('admin/news_list.html', news=news)


# 删除功能实现
class DelNews(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self, id=None):
        if id:
            news = db.session.query(News).get(id)  # 如果有id 从数据库读取这个id项
            if news:
                db.session.delete(news)  # 如果有这个项  删除此项
                db.session.commit()
        return redirect(url_for('admin.news_list'))


# 文章创建编辑
class NewsCreateOrEdit(MethodView):
    decorators = [login_required]  # 相当于 @login_required 装饰圈

    def get(self, id=None):
        news = News() if not id else db.session.query(News).get(id)  # 如果没有id创建实例，如果有数据库读取这个id项
        form = NewsForm(request.form) if not id else NewsForm(obj=news)  # 如果没有id 请求表单项内容，如果有表单内容是从数据库得到
        # form.log_category_id.choices = [(d.id, d.category) for d in Log_Category.query.all()]  # 分类从数据库查询到 做推导
        return render_template('admin/write-article.html', form=form)

    def post(self, id=None):
        form = NewsForm()  # 请求表单项内容
        news = News() if not id else db.session.query(News).get(id)  # 如果没有id创建实例，如果有数据库读取这个id项
        news.name = form.name.data
        news.content = form.content.data
        if form.img.data:
            news.img = form.img.data.filename
            f = form.img.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
        if not id:
            db.session.add(news)  # 向数据库添加
            db.session.commit()
        else:
            db.session.commit()
        return redirect(url_for('admin.news_list'))
