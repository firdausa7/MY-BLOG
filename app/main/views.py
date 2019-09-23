from flask import render_template, request, redirect, url_for, flash
from . import main
from app import db
from ..requests import get_quotes
from flask_login import login_required, current_user
from .forms import CreateBlog, AddComment, EditBlog, SubscribeForm
from ..models import User, Blog, Comment,Subscription
@main.route('/', methods=['GET', 'POST'])
def index():
    new_quote = get_quotes()
    blogs = Blog.query.all()
    users = User.query.all()
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        subscription = Subscription(email=email)
        db.session.add(subscription)
        db.session.commit()
        return render_template('index.html', new_quote=new_quote, blogs=blogs, users=users, subscribe_form=form)
    return render_template('index.html', new_quote=new_quote, blogs=blogs, users=users, subscribe_form=form)


@main.route('/blog/<id>', methods=["get", "post"])
def blog(id):
    comment_form = AddComment()
    blog = Blog.query.filter_by(id=id).first()
    if comment_form.validate_on_submit():
        feedback = comment_form.comment.data
        comment = Comment(feedback=feedback,
                          user_id=current_user.id, blog_id=id)
        db.session.add(comment)
        db.session.commit()
        comments = Comment.query.filter_by(blog_id=id).all()
        return render_template("blog.html", blog=blog, comments=comments, comment_form=comment_form)
    comments = Comment.query.filter_by(blog_id=id)
    return render_template("blog.html", blog=blog, comment_form=comment_form, comments=comments)


@main.route('/addblog', methods=["get", "post"])
def add_blog():
    blogform = CreateBlog()

    if blogform.validate_on_submit():

        title = blogform.title.data
        subtitle = blogform.subtitle.data
        body = blogform.body.data
        new_blog = Blog(title=title, subtitle=subtitle,
                        body=body, user_id=current_user.id)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_blog.html', blog_form=blogform)


@main.route('/profile/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    blogs = Blog.query.filter_by(user_id=user.id).all()
    return render_template("profile/profile.html", user=user, blogs=blogs)


@main.route('/deleteComment/<int:commentid>/<int:blogid>', methods=["get", "post"])
def deleteComment(commentid, blogid):
    comment = Comment.query.filter_by(id=commentid).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("main.blog", id=blogid))


@main.route('/deleteblog/<blogid>', methods=["get", "post"])
def delete_blog(blogid):
    blog = Blog.query.filter_by(id=blogid).first()
    uname = current_user.username
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for("main.profile", uname=uname))


@main.route('/editblog/<blogid>', methods=["get", "post"])
def edit_blog(blogid):

    form = EditBlog()

    if form.validate_on_submit():
        body = form.body.data
        blog = Blog.query.filter_by(id=blogid).update({"body": body})
        db.session.commit()
        return redirect(url_for("main.profile", uname=current_user.username))
    else:
        form.body.data = Blog.query.filter_by(id=blogid).first().body
    return render_template("update_blog.html", updateblog_form=form)
