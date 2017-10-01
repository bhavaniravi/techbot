from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask import Flask
from sqlalchemy_utils.types.choice import ChoiceType
from flask_admin import Admin


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


db = SQLAlchemy(app)
migrate = Migrate(app, db)


admin = Admin(app, name='newsbot-KB', template_mode='bootstrap3')


CATEGORIES = ['blog',
 'jobs',
 'modules',
 'applications',
 'related skills',
 'github projects',
 'frameworks',
 'python trivia',
 'python news']

class Info(db.Model):
    TYPES = ()
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80))#ChoiceType([(category,category) for category in CATEGORIES]))
    title = db.Column(db.Text)
    link = db.Column(db.Text)


class MyModelView(ModelView):
    def __init__(self, model, session, name=None, category=None, endpoint=None, url=None, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        super(MyModelView, self).__init__(model, session, name=name, category=category, endpoint=endpoint, url=url)
    form_choices = {'category': [(category,category) for category in CATEGORIES]}

admin.add_view(MyModelView(Info, db.session))
