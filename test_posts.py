from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BlogsTestCase(TestCase):
    """Tests for views for Blogly."""

    def test_list_posts(self):
        user = User(first_name="Lua", last_name="Montana", image_url="")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id
        post = Post(title="Lucky", content="I found a treasure in the forest.", user_id=user.id)
        db.session.add(post)
        db.session.commit()
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}/")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3>Lua Montana</h3>', html)


    def test_show_post(self):
        with app.test_client() as client:
            res = client.get(f"/posts/1")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>title</h1>', html)


    def test_add_post(self):
        with app.test_client() as client:
            user = User(first_name="Luna", last_name="Saturni", image_url="")
            db.session.add(user)
            db.session.commit()
            p = {"title": "title", "content":"content", "user_id": 1}
            res = client.post("/users/1/posts/new", data=p, follow_redirects=True)
            html = res.get_data(as_text=True)
            #print(html)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Add post", html)