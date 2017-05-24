from flask_script import Manager, Server, prompt_bool
import config
from app import create_app
from app.model import db

app = create_app(config.Config)

manager = Manager(app)
manager.add_command('runserver', Server(host='127.0.0.1', port=8000))


@manager.command
def create_db():  # 创建db
    db.create_all()


@manager.command
def drop_db():  # 删除db
    if prompt_bool('你确定删除数据库吗?'):
        db.drop_all()


@manager.command
def recreate_db():  # 重新创建db
    drop_db()
    create_db()


if __name__ == '__main__':
    manager.run()
