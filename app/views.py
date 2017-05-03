from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.socketio import emit
from app import socketio
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from .forms import LoginForm, ProjectForm, InviteForm
from .user import User


@app.route('/')
@login_required
def home():
    return render_template('home.html', projects=getProjects())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'], user['name'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("home"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProjectForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            seqid = getNextSequence("projectid")
            result = app.config['PROJECTS_COLLECTION'].insert_one(
                {
                    "_id": seqid,
                    "name": form.projectname.data,
                    "description": form.projectdescription.data,
                    "owner": current_user.username
                }
            )
            app.config['USERS_COLLECTION'].find_one_and_update(
                {'_id': current_user.username },
                {'$push': {'projects': seqid}}
            )
            app.config['USERS_COLLECTION'].update_many(
                {'role': 'admin' },
                {'$push': {'projects': seqid}}
            )
            flash("Project Created!", category='success')
            return redirect(request.args.get("next") or url_for("create"))
        except DuplicateKeyError:
            flash("Could not create project!", category='error')
    return render_template('create.html', form=form, projects=getProjects())

@app.route('/project/<projectid>')
@login_required
def project(projectid):
    form = InviteForm()
    result = app.config['USERS_COLLECTION'].find_one({'$and': [{"_id": current_user.username}, {'projects': int(projectid)}]})
    if result == None:
        flash("You don't have permission to view this project!", category='error')
        return redirect(request.args.get("next") or url_for("home"))
    proj = app.config['PROJECTS_COLLECTION'].find_one({"_id": int(projectid)})
    users = app.config['USERS_COLLECTION'].find({'$and': [{"role": {'$ne':'admin'}}, {'projects': {'$ne': int(projectid)}}]})
    form.inviteusers.choices = [(user['_id'], user['name']) for user in users]
    return render_template('project.html', proj=proj, projects=getProjects(), form=form, users=users)


@app.route('/invite/<projectid>', methods=['POST'])
@login_required
def invite(projectid):
    form = InviteForm()
    username=""
    if request.method == 'POST':
        username = form.inviteusers.data
    result = app.config['USERS_COLLECTION'].find_one({'$and': [{"_id": current_user.username}, {'$or': [{'role': 'admin'}, {'$and':[{'role': 'manager'}, {'projects': int(projectid)}]}]}]})
    if result == None:
        flash("You don't have permission to invite others to this project!", category='error')
        return redirect(url_for("project", projectid=projectid))
    app.config['USERS_COLLECTION'].find_one_and_update({ '_id': username }, {'$addToSet': {'projects': int(projectid)}})
    flash("User invited successfully!", category='success')
    socketio.emit('invited', {'data': {'invited', projectid}}, room = 'user_' + username)
    return redirect(url_for("project", projectid=projectid))

@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'], u['name'])

def getNextSequence(name):
    ret = app.config['COUNTER_COLLECTION'].find_one_and_update(
            { '_id': name },
            { '$inc': { 'seq': 1 } },
            return_document=ReturnDocument.AFTER
        )

    return ret['seq']

def getProjects():
    user = app.config['USERS_COLLECTION'].find_one({"_id": current_user.username})
    projects = app.config['PROJECTS_COLLECTION'].find({"_id" : {"$in" :user['projects']}})
    project_list = []
    for x in projects:
        project_list.append((x['_id'],x['name']))
    return project_list
