from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.blog import Blog

@app.route('/new/blog')
def new_blog():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('create_blog.html', user = User.get_user_by_id(data))

@app.route('/create/blog', methods = ["POST"])
def create_blog():
    if not Blog.validate_blog(request.form):
        return redirect('/new/blog')
    blog_data = {
        "user_id": session['user_id'],
        "name": request.form['name'],
        "topic": request.form['topic'],
        "description": request.form['description']
    }
    Blog.save_blog(blog_data)
    return redirect('/home')