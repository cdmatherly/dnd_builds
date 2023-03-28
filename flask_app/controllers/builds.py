from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.build import Build


@app.route('/builds/save', methods=['POST'])
def save_build():
    # print(f"FORM DATA >>>>> {request.form}")
    data = {
        **request.form,
        'img_path': request.form['race'].lower() + '-' + request.form['buildClass'].lower()
    }
    Build.create_build(data)
    return redirect(f"/users/{session['user_id']}/builds")

@app.route('/builds/delete/<int:build_id>')
def delete_build(build_id):
    Build.delete_build(build_id)
    return redirect(f"/users/{session['user_id']}/builds")

@app.route('/builds/edit/<int:build_id>')
def edit_build(build_id):
    this_build = Build.get_build_by_id(build_id)
    print(this_build.proficiencies)
    return render_template("edit_build.html", build = this_build)

@app.route('/builds/update', methods=['POST'])
def update_build():
    newList = Build.listify(request.form) #take the input and run in through listify, reassign proficiencies
    print(f"New List >>>> {newList}")
    # request.form['proficiencies'] = newList
    data = {
        **request.form,
        'proficiencies': newList
    }
    print(data)
    Build.update_build(data)
    return redirect(f"/users/{session['user_id']}/builds")