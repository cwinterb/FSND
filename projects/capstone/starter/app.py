#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Actor, Project
from constants import SQLALCHEMY_DATABASE_URI, login_url
from flask_migrate import Migrate
from flask_wtf import Form
from forms import *
from auth import AuthError, requires_auth
import json
from werkzeug.exceptions import HTTPException
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode

# from authlib.flask.client import OAuth

#----------------------------------------------------------------------------#
# App configuration
#----------------------------------------------------------------------------#


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r"/api/": {"origins": "*"}})
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    setup_db(app)

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id='niAAnrxzVlTXC5J3K76pLItw8JiSj9LV',
        client_secret='ye3vSQcDIgwG0ZEttdWMf5rx6NgN3tQVhg_C3fqPE_OygzTepUxfomjDZsGK3h9O',
        api_base_url='https://cwinterb.auth0.com',
        access_token_url='https://cwinterb.auth0.com/oauth/token',
        authorize_url='https://cwinterb.auth0.com/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/callback')
    def callback_handling():
        # Handles response from token endpoint
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()
        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        return redirect('/')

#----------------------------------------------------------------------------#
# Endpoints
#----------------------------------------------------------------------------#

    # home route
    @app.route('/')
    def index():
        return render_template('home.html')

#----------------------------------------------------------------------------#
# Login
#----------------------------------------------------------------------------#

    @app.route('/login')
    def login():
        # return redirect(login_url)
        return auth0.authorize_redirect(redirect_uri='http://localhost:8080/callback')

#----------------------------------------------------------------------------#
# Actors Endpoints
#----------------------------------------------------------------------------#

    # gets all actors and posts a new actor
    @app.route('/actors', methods=["GET"])
    @requires_auth('get:actors')
    def actors(token):
        return render_template('pages/actors.html', actors=Actor.query.all())

    @app.route('/actors', methods=["POST"])
    @requires_auth('post:actors')
    def post_actor(token):
        try:
            name = request.form.get("name")
            age = request.form.get("age")
            gender = request.form.get("gender")
            new_actor = Actor(name=name, age=age, gender=gender)
            db.session.add(new_actor)
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
            return render_template('pages/actors.html')

    # gets the form for posting a new actor profile:
    @app.route('/actors/create', methods=["GET"])
    @requires_auth('post:actors')
    def create_actor(token):
        form = ActorForm()
        return render_template('forms/post_actor.html', form=form)

    # gets an actor's profile
    @app.route('/actors/<int:id>', methods=["GET"])
    @requires_auth('get:actors')
    def show_actor(token, id):
        actor = Actor.query.filter_by(id=id).first()
        return render_template('pages/actor_profile.html', actor=actor)

    # edits existing actor:
    @app.route('/actors/<int:id>/edit', methods=["POST"])
    @requires_auth('patch:actor')
    def edit_actor(token, id):
        try:
            actor = Actor.query.filter_by(id=id).first()
            actor.name = request.form.get("name")
            actor.age = request.form.get("age")
            actor.gender = request.form.get("gender")
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
            return redirect(url_for('actors'))

    # deletes actor
    @app.route('/actors/<int:id>', methods=["POST"])
    @requires_auth('delete:actor')
    def delete_actor(token, id):
        if request.method == "POST":
            try:
                actor = Actor.query.filter(Actor.id == id).one_or_none()
                if actor is None:
                    return jsonify({"message": "actor not found"})
                actor.delete()
            except:
                db.session.rollback()
                return jsonify({
                    "message": "there was an error deleting"
                })
            finally:
                db.session.close()
                return redirect(url_for('actors'))

    # gets the form for editing an actor profile
    @app.route('/actors/<int:id>/edit', methods=["GET"])
    def get_edit_actor(id):
        actor = Actor.query.filter_by(id=id).one()
        form = ActorForm()
        return render_template('forms/edit_actor.html', actor=actor, form=form)

#----------------------------------------------------------------------------#
# Projects Endpoints
#----------------------------------------------------------------------------#
    # get all projects and post a new project
    @app.route('/projects', methods=["GET"])
    @requires_auth('get:projects')
    def projects(token):
        if request.method == "GET":
            return render_template('pages/projects.html', projects=Project.query.all())
        if request.method == "POST":
            try:
                title = request.form.get("title")
                release_date = request.form.get("release_date")
                new_project = Project(title=title, release_date=release_date)
                db.session.add(new_project)
                db.session.commit()
            except:
                db.session.rollback()
                abort(422)
            finally:
                db.session.close()
                return redirect(url_for('projects'))

    # deletes a project profile
    @app.route('/projects/<int:id>/delete', methods=["POST"])
    @requires_auth('delete:project')
    def delete_project(token, id):
        try:
            project = Project.query.filter(Project.id == id).one_or_none()
            if project is None:
                return jsonify({"message": "project not found"})
            project.delete()
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({
                "message": "there was an error deleting"
            })
        finally:
            db.session.close()
            return redirect(url_for('projects'))

    @app.route('/projects/<int:id>/update', methods=["POST"])
    @requires_auth('patch:project')
    def update_project(token, id):
        try:
            project = Project.query.filter_by(id=id).first()
            project.title = request.args.get("title")
            project.release_date = request.args.get("release_date")
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
            return redirect(url_for('projects'))

    @app.route('/projects/create')
    def get_project_create():
        form = ProjectForm()
        return render_template('forms/post_project.html', form=form)

    @app.route('/projects/<int:id>', methods=["GET"])
    def get_project_profile(id):
        project = Project.query.filter_by(id=id).first()
        return render_template('pages/project_profile.html', project=project)

    @app.route('/projects/<int:id>/edit')
    def get_edit_project(id):
        project = Project.query.filter_by(id=id).first()
        form = ProjectForm()
        return render_template('pages/edit_project.html', project=project, form=form)

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
