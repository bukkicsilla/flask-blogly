from unittest import TestCase

from app import app
from models import db, User, Post, Tag

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

    def setUp(self):
        """Add sample blog."""
        Tag.query.delete()
        tag = Tag(name="Cat")
        db.session.add(tag)
        db.session.commit()
        self.tag_id = tag.id


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_list_tags(self):
        with app.test_client() as client:
            res = client.get("/tags")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Tags</h1>', html)


    def test_show_tag(self):
        with app.test_client() as client:
            res = client.get(f"/tags/{self.tag_id}")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Cat</h1>', html)


    def test_add_tag(self):
        with app.test_client() as client:
            t = {"name": "Happy"}
            res = client.post("/tags/new", data=t, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Tags</h1>", html)