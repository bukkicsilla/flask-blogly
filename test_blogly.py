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

    def setUp(self):
        """Add sample blog."""
        User.query.delete()
        user = User(first_name="Kathy", last_name="Rainy", image_url="")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Kathy', html)


    def test_show_user(self):
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}/")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3>Kathy Rainy</h3>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Kathy", "last_name": "Rainy", "image_url":""}
            res = client.post("/users/new", data=d, follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Add user", html)

    def test_greet(self):
        User.query.delete()
        user = User(first_name="Luna", last_name="White")
        self.assertEquals(user.greet(), "Hello, you can have a friend called Luna White.")