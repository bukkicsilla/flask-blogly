"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = "Be kind whenever possible. It is always possible."
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 10
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route("/")
def home():
    '''Redirected to /users'''
    return redirect("/users")

@app.route("/users")
def users_list():
    '''Shows all the users'''
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route("/users/new")
def show_create_form_user():
    return render_template('new_user.html')

@app.route("/users/new", methods=['POST'])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    if not first_name:
        flash("Firstname cannot be empty!", "invalid")
        return redirect("/users")
    if not last_name:
        flash("Lastname cannot be empty!", "invalid")
        return redirect("/users")
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/")
def show_user(user_id):
    '''Shows details about a single user'''
    user = User.query.get(user_id)
    greeting = user.greet()
    posts = User.query.get(user_id).posts
    return render_template('user.html', user=user, greeting=greeting, posts=posts)

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    '''Deletes a singe user'''
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    '''Modify details about a single user'''
    user = User.query.filter_by(id=user_id).first()
    if not user.image_url:
        user.image_url = ""
    return render_template('edit_user.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=['POST'])
def edit_user(user_id):
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    if not first_name:
        flash("Firstname cannot be empty!", "invalid")
        return redirect(f"/users/{user_id}")
    if not last_name:
        flash("Lastname cannot be empty!", "invalid")
        return redirect(f"/users/{user_id}")
    user = User.query.filter_by(id=user_id).first()
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/users/<int:user_id>/posts/new")
def show_create_form_post(user_id):
    user = User.query.get(user_id)
    return render_template('new_post.html', user=user)

@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def create_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    if not title:
        flash("Title cannot be empty!", "invalid")
        return redirect(f"/users/{user_id}")
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    '''Deletes a singe post'''
    post = Post.query.get(post_id)
    user_id = post.user_id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>/edit")
def show_edit_form_post(post_id):
    post = Post.query.get(post_id)
    return render_template("edit_post.html", post=post)

@app.route("/posts/<int:post_id>/edit" , methods=['POST'])
def edit_post(post_id):
    title = request.form["title"]
    content = request.form["content"]
    if not title:
        flash("Title cannot be empty!", "invalid")
        return redirect(f"/posts/{post_id}")
    post = Post.query.get(post_id)
    post.title = title
    post.content = content
    post.user_id = post.user.id
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")


