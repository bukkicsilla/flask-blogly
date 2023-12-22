from models import db, User, Post
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name="Fluffy", last_name="Lazarus")
u2 = User(first_name="Donut", last_name="Sing")
u3 = User(first_name="Moomoo", last_name="White")
#db.session.add(u1)
#db.session.add(u2)
#db.session.add(u3)
db.session.add_all([u1, u2, u3])
db.session.commit()


p1 = Post(title="calici", content="I was sick because of the calicivirus.", user_id = 1 )
p2 = Post(title="joy", content="I am a happy male cat. My owner loves me very much.", user_id=1)
p3 = Post(title="wild", content="I love to be outside, even at night.", user_id=2)
p4 = Post(title='loyal', content="I love my owner, and I like to be in the room.", user_id=3)
db.session.add_all([p1, p2, p3, p4])
db.session.commit()