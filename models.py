#https://www.reddit.com/r/flask/comments/ypqk40/default_datetimenow_not_using_current_time/
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly.""" 
    
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.Text, nullable=True, default=None)
    #posts = db.relationship('Post', backref='user', cascade="all, delete, delete-orphan")
    #posts = db.relationship("Post", back_populates="user", cascade="all, delete", passive_deletes=True)
    #posts = db.relationship('Post', back_populates="user", cascade='all, delete, delete-orphan')

    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    

    def greet(self):
        return f"Hello, you can have a friend called {self.first_name} {self.last_name}."
    

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"
    

    @fullname.setter
    def fullname(self, first_name, last_name):
        self._fullname = f"{first_name} {last_name}"

    @fullname.deleter
    def fullname(self):
        del self._fullname

    

class Post(db.Model):
    __tablename__ = "posts"

    def __repr__(self):
        return f"<Post {self.title} {self.content} {self.created_at}>"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    #user = db.relationship("User", back_populates="posts")
    user = db.relationship('User', backref='posts')
    #user = db.relationship('User', backref=db.backref('posts', passive_deletes=True))

    @property
    def nicedate(self):
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    

#https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete
#https://stackoverflow.com/questions/26475977/flask-sqlalchemy-adjacency-list-backref-error