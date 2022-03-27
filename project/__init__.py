import warnings
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)

app.secret_key = '@p2ploans'

# The config is actually a subclass of a dictionary and can be modified just like any dictionary

app.config['TESTING'] = True

# If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals.
# The default is None, which enables tracking but issues a warning that
# it will be disabled by default in the future.
# This requires extra memory and should be disabled if not needed.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# If set to True SQLAlchemy will log all the statements issued to stderr which can be useful for debugging.
app.config['SQLALCHEMY_ECHO'] = True

# In debug mode Flask-SQLAlchemy will log all the SQL queries sent to the database.
# This information is available until the end of request
# which makes it possible to easily ensure that the SQL generated is the one expected on errors or in unittesting.
app.config['SQLALCHEMY_RECORD_QUERIES'] = True

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/pythondb'

# Controls the number of connections that can be created after the pool reached its maximum size.
# When those additional connections are returned to the pool, they are disconnected and discarded.
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0

db = SQLAlchemy(app)

import project.com.controller
