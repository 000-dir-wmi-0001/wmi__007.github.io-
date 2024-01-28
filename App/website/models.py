# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from sqlalchemy.sql import func

# db = SQLAlchemy()

# class ThemeColor(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     color = db.Column(db.String(100))
#     click_count = db.Column(db.Integer, default=0)
#     note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
#     note = db.relationship('Note', back_populates='theme_color')

# class Recording(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime(timezone=True), default=func.now, onupdate=func.now)
#     filename = db.Column(db.String(255))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', back_populates='recordings')
   


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     theme_color = db.relationship('ThemeColor', back_populates='note', uselist=False)
#     date = db.Column(db.DateTime(timezone=True), default=func.now, onupdate=func.now)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship('User', back_populates='notes')

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     user_name = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(150))
#     recordings = db.relationship('Recording', back_populates='user')
#     notes = db.relationship('Note', back_populates='user')


from anyio import Event
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy()

# class ThemeColor(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     color = db.Column(db.String(100))

class Recording(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    filename = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    clickCount = db.Column(db.Integer)
    user = db.relationship('User', back_populates='recordings')
    
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # theme_color_id = db.Column(db.Integer, db.ForeignKey('theme_color.id'), unique=True)
    clickCount = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now, onupdate=func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='notes')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150))
    recordings = db.relationship('Recording', back_populates='user')
    notes = db.relationship('Note', back_populates='user')
    

