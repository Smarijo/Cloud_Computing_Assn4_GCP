from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
 
login = LoginManager()
db = SQLAlchemy()
 
class UserInfo(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String())

 
 
@login.user_loader
def load_user(id):
    return UserInfo.query.get(int(id))

