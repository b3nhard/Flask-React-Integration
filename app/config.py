import os

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    SECRET_KEY = "ffGpqsJjn/cPNV/VVMN+pUBEHMxpprKzgJI27a5rghXg9XFG/p0LDYPnxrw0w8Vp"
    STATIC_FOLDER = os.path.join(basedir,"build/static")
    TEMPLATE_FOLDER = os.path.join(basedir,"build")



config = Config

