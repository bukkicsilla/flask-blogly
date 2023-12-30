#https://www.reddit.com/r/flask/comments/ypqk40/default_datetimenow_not_using_current_time/
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly.""" 
    
class User(db.Model):
    """Create a user"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.Text, nullable=True, default=None)
    #posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    #posts = db.relationship("Post", backref="user", cascade="all, delete")

    
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
    """Post by a user"""

    __tablename__ = "posts"

    def __repr__(self):
        return f"<Post {self.title} {self.content} {self.created_at}>"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='posts')
    #user = db.relationship(
    #    "User", backref=db.backref("posts", cascade="all, delete-orphan")
    #)

    @property
    def nicedate(self):
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tag that can be added to a post."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        #cascade="all,delete",
        backref="tags",
    )

#https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete
#https://stackoverflow.com/questions/26475977/flask-sqlalchemy-adjacency-list-backref-error