import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from notes import file_manager, directory_manager, activity, db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)

    api = Api(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'notes.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # with app.app_context():
    #     db.init_db()

    api.add_resource(file_manager.File, '/file/<filename>')
    api.add_resource(directory_manager.Directory, '/ls')
    api.add_resource(activity.Activity, '/activity')

    return app
