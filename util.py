from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def connect_db(path, dbName):
    # 建立数据库连接
    cmd = 'sqlite:///' + path + '/db/' + dbName + '.db'
    engine = create_engine(cmd)
    DBSession = sessionmaker(bind=engine)
    return engine, DBSession


def create_session(path, dbName):
    cmd = 'sqlite:///' + path + '/db/' + dbName + '.db'
    engine = create_engine(cmd)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session