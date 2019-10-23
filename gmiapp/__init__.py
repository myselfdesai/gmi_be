from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SECRET_KEY'] = '6e0a487c88c3934867788e2b2691543b' # this should be stored in sys environment for security 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db = SQLAlchemy(app)
ma = Marshmallow(app)

from gmiapp import routes