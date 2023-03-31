from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.build import Build


@app.route('/builds/save', methods=['POST'])
def save_build():
    # print(f"FORM DATA >>>>> {request.form}")
    if 'user_id' not in session:
        session['race'] = request.form['race']
        session['buildClass'] = request.form['buildClass']
        session['background'] = request.form['background']
        session['proficiencies'] = request.form['proficiencies']
        session['raceDescription'] = request.form['raceDescription']
        session['bgDescription'] = request.form['bgDescription']
        print(session)
        return redirect('/users/register')
    user_builds = Build.get_builds_by_user(session['user_id']) #check how many builds are currently saved
        
    data = {
        **request.form,
        'img_path': request.form['race'].lower() + '-' + request.form['buildClass'].lower(),
        'build_name': Build.make_build_name(user_builds) 
    }
    # print(data)
    new_build_id = Build.create_build(data)
    session['new_build_id'] = new_build_id
    return redirect(f"/users/{session['user_id']}/builds")

@app.route('/builds/save/held')
def save_held_build():
    # print(f"FORM DATA >>>>> {request.form}")
    # if 'user_id' not in session:
    #     session['race'] = request.form['race']
    #     session['buildClass'] = request.form['buildClass']
    #     session['background'] = request.form['background']
    #     session['proficiencies'] = request.form['proficiencies']
    #     session['raceDescription'] = request.form['raceDescription']
    #     session['bgDescription'] = request.form['bgDescription']
    #     print(session)
    #     return redirect('/users/register')
    user_builds = Build.get_builds_by_user(session['user_id']) #check how many builds are currently saved
        
    data = {
        **session,
        'img_path': session['race'].lower() + '-' + session['buildClass'].lower(),
        'build_name': Build.make_build_name(user_builds) 
    }
    # print(data)
    Build.create_build(data)
    session.pop('race')
    session.pop('buildClass')
    session.pop('background')
    session.pop('proficiencies')
    session.pop('raceDescription')
    session.pop('bgDescription')
    return redirect(f"/users/{session['user_id']}/builds")

@app.route('/builds/delete/<int:build_id>')
def delete_build(build_id):
    deleted_build = Build.get_build_by_id(build_id)
    next_build = Build.find_next_build(deleted_build)
    Build.delete_build(build_id)
    session['new_build_id'] = next_build.id
    return redirect(f"/users/{session['user_id']}/builds")

@app.route('/builds/edit/<int:build_id>')
def edit_build(build_id):
    this_build = Build.get_build_by_id(build_id)
    # print(this_build.proficiencies)
    session['new_build_id'] = build_id
    return render_template("edit_build.html", build = this_build)

@app.route('/builds/update', methods=['POST'])
def update_build():
    newProf = Build.listify(request.form['proficiencies']) #take the input and run in through listify, reassign proficiencies // returns string
    # is_valid = Build.validate(request.form)
    # if not is_valid:
    #     return redirect(f"/builds/edit/{request.form['id']}")
    # print(f"New String >>>> {newProf}")
    data = {
        **request.form,
        'proficiencies': newProf, #overwrite proficiencies with our string version
        'img_path': request.form['race'].lower() + '-' + request.form['build_class'].lower()
    }
    # print(data)
    Build.update_build(data) #pass through info from the form and 
    return redirect(f"/users/{session['user_id']}/builds")