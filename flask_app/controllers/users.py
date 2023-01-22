from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.blog import Blog
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login_and_register.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('home.html', user = User.get_user_by_id(data), blogs = Blog.get_all_blogs_with_creator())


@app.route('/register/user', methods = ["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save_user(data)
    session['user_id'] = user_id
    return redirect('/home')

@app.route('/login/user', methods = ["POST"])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash ("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    