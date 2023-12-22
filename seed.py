from models import db, User, Post
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name="Fluffy", last_name="Lazarus", image_url="https://images.unsplash.com/photo-1573865526739-10659fec78a5?q=80&w=2815&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
u2 = User(first_name="Donut", last_name="Sing", image_url="https://images.unsplash.com/photo-1618826411640-d6df44dd3f7a?q=80&w=2048&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
u3 = User(first_name="Moomoo", last_name="White", image_url="https://images.unsplash.com/photo-1612632237538-2de30e25af6f?q=80&w=2835&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
#db.session.add(u1)
#db.session.add(u2)
#db.session.add(u3)
db.session.add_all([u1, u2, u3])
db.session.commit()


p1 = Post(title="calici", content="I was sick because of the calicivirus.", user_id = 1 )
p2 = Post(title="joy", content="I am a happy male cat. My owner loves me very much.", user_id=1)
p3 = Post(title="wild", content="I love to be outside, even at night.", user_id=2)
p4 = Post(title='loyal', content="I love my owner, and I like to be in the room.", user_id=3)
p5 = Post(title="tiger", content="I have stripes. I look like a tiger.", user_id=2)
p6 = Post(title='sweet', content="I have a long black and white hair, you can pet me.", user_id=3)
db.session.add_all([p1, p2, p3, p4, p5, p6])
db.session.commit()