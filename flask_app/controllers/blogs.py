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
    if 'user_id' not in session:
        return redirect('/')
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


@app.route('/user/account')
def user_profile():
    if 'user_id' not in session:
        return redirect('/')
    id = {
        "id": session['user_id']
    }
    user = User.get_one_user_with_blogs(id)
    return render_template('user_account.html', user = user)

@app.route('/edit/<int:id>')
def edit_blog(id):

    return render_template('edit_blog.html')

@app.route('/update/<int:id>', methods = ["POST"])
def update_blog(id):

    return redirect('/user/account')

@app.route('/delete/<int:id>')
def delete_blog(id):

    return redirect('/user/account')

@app.route('/show/<int:id>')
def show_blog(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    blog_id = {
        "id": id
    }
    one_blog = Blog.get_one_blog_with_user(blog_id)
    
    return render_template('view_blog.html', one_blog = one_blog, user = User.get_user_by_id(data))