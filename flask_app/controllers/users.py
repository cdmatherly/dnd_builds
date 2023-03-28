from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.build import Build

@app.route('/')
def index():
    if 'user_id' in session:
        logged_user = User.get_user_by_id(session['user_id'])
        # print(logged_user)
    else:
        logged_user = 0
    return render_template('generate.html', user = logged_user)

@app.route('/users/login')
def go_to_login():
    return render_template('login.html')

@app.route('/users/register')
def go_to_register():
    return render_template('register.html')

@app.route('/users/create', methods=['POST'])
def create_user():
    if not User.validate(request.form):
        return redirect('/users/register')
    if User.check_user(request.form):
        return redirect('/users/register')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    user_data = {
        **request.form,
        'password' : hashed_pw
    }
    user_id = User.save(user_data)
    session['user_id'] = user_id

    return redirect('/')

@app.route('/users/login/go', methods=['POST'])
def login_user():
    user_in_db = User.get_user_by_email(request.form)
    if not user_in_db:
        flash('User not found', 'login')
        return redirect('/users/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid login credentials', 'login')
        return redirect('/users/login')
    session['user_id'] = user_in_db.id
    return redirect('/')

# @app.route('/dashboard')
# def show_dash():
#     if 'user_id' not in session:
#         return redirect('/')
    
#     logged_user = User.get_user_by_id(session['user_id'])
#     # print(logged_user)

#     return render_template('generate.html', user = logged_user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/generate')
def go_to_generate():
    return render_template('generate.html')

@app.route('/users/<int:user_id>/builds')
def show_builds(user_id):
    if not "user_id" in session:
        return redirect('/')
    user = User.get_user_by_id(user_id)
    all_builds = Build.get_builds_by_user(user_id)
    # print(all_builds)
    return render_template('saved_builds.html', user = user, all_builds = all_builds)
