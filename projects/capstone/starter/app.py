import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Actor, Project
from constants import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    setup_db(app)

    @app.route('/')
    def index():
        return render_template('home.html')

    @app.route('/actors', methods=["GET", "POST"])
    def actors():
        if request.method == "GET":
            # return render_template('pages/actors.html', actors=Actor.query.all())
            actors = Actor.query.all()
            actors_list = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'actors': actors_list,
                'code': 200
            })
        if request.method == "POST":
            try:
                name = request.args.get("name")
                print(name)
                age = request.args.get("age")
                print(age)
                gender = request.args.get("gender")
                print(gender)
                new_actor = Actor(name=name, age=age, gender=gender)
                db.session.add(new_actor)
                db.session.commit()
            except DatabaseError:
                db.session.rollback()
                abort(422)
            finally:
                db.session.close()
                return jsonify({
                    'name': name,
                    'age': age,
                    'gender': gender
                })

    @app.route('/actors/<int:id>', methods=["PATCH"])
    def update_actor(id):
        try:
            actor = Actor.query.filter_by(id=id).first()
            print(actor)
            actor.name = request.args.get("name")
            print(actor.name)
            actor.age = request.args.get("age")
            print(actor.age)
            actor.gender = request.args.get("gender")
            print(actor.gender)
            print(actor.__dict__)
            db.session.commit()
        except DatabaseError:
            print("database error")
            db.session.rollback()
            abort(422)
        finally:
            print(actor.__dict__)
            db.session.close()
            return jsonify({
                'code': 'success'
            })
    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
