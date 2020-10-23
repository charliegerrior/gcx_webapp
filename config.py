import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    #REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
    #REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False