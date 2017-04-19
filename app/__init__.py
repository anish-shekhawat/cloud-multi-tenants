from flask import Flask
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
app.config['COUNTER_COLLECTION'].find_one_and_update(
        { '_id': "projectid" },
        { '$setOnInsert': { 'seq': 0 }},
        upsert= True
    )

from app import views
