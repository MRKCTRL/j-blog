from flask import Flask, render_template, redirect, url_for, flash, g, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm
from flask_gravatar import Gravatar
from functools import wraps
# from flask import g, request, redirect, url_for
# from sqlalchemy import Table, Column, Integer, foreignKey
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)
# sqlalchemy
# Base = declarative_base()
Bootstrap(app)

gravatar = Gravatar(app, size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None
                    )

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ----------- User db
class User(UserMixin, db.Model):
    __table__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    post = relationship('BlogPost', back_populates='author')

    # how to create parent to child
    comments = relationship('Comment', back_populates=comment_author)

    #
    # def __init__(self, arg):
    #     superUser, self).__init__()
    #     self.arg = arg

    # comment Table

    class Comment(db.Model):
        __table__ = 'comments'
        id = db.Column(db.Integer, primary_key=True)

        author_id = db.Column(db.Integer, db.foreignKey('users.id'))
        comment_author = relationship('User', back_populates='comments')
        # text = db.Column(db.String(100))

        post_id = db.Column(db.Integer, db.foreignKey('blog_posts.id'))
        parent_post = relationship('BlogPost', back_populates='comments')
        text = db.Column(db.Text, nullable=False)
        # text =

        # post = relationship('BlogPost', back_populates='author')
        # author_id = db.Column(db.Integer, db.foreignKey('users.id'))
        #
        # author = relationship('User', back_populates='posts'


# relationship between comment and user
# class User(db.model):
#     __table__ = 'user'
#     id =
#     author


# CONFIGURE TABLES

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.foreignKey('users.id'))

    author = relationship('User', back_populates='posts')

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    # child to parent relationship
    commenting = relationship('Comment', back_populates='parent_post')


db.create_all()


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=request.form.get('email')).first():
            flash('You have already signed up with that email, log in stead!')
            return redirect(url_for('login'))

        hash_and_salt = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salt,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('get_all_posts'))

        # return redirect(url_for('get_all_posts'))
    return render_template("register.html", form=form, current_user=current_user)


# ------- admin deco
# @app.errorhandler(404)
# def page_not(e):
#     return render_template('404.html'), 404
@app.route('/new-post')
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.user.id != 1:
            return abort(403)
            # return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# admin_only =
# admin_only,init(app)


# TODO: edit index, envir variables day 35, FLASK AND GITINGORE
# ------------ login
login_manager = LoginManager()
login_manager.init(app)


#  I forgot the below cod
@login_required.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
@login_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('that email does not exist, please try again')
            return redirect(url_for('login'))

        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))
    # redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>")
@login_required
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    if form.validate_on_submit():
        if not current_user_is_authenticated:
            Flash('You need to login or register to comment')
            return redirect(url_for('login'))

        new_comment = Comment(
            text=form.comment_text.data,
            comment=current_user,
            parent_post=requested_post
        )
        db.session(new_comment)
        db.session.commit()

    return render_template("post.html", post=requested_post, form=form, current_user=current_user)


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)


@app.route("/new-post")
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, current_user=current_user)


@app.route("/edit-post/<int:post_id>")
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
