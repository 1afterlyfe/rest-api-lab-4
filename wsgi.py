from flask import Flask, jsonify
from flask_smorest import Api
from extensions import db, migrate

from resources.users import blp as UsersBlueprint
from resources.categories import blp as CategoriesBlueprint
from resources.records import blp as RecordsBlueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py", silent=False)

    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)

    api.register_blueprint(UsersBlueprint)
    api.register_blueprint(CategoriesBlueprint)
    api.register_blueprint(RecordsBlueprint)

    @app.route("/")
    def index():
        return jsonify({"message": "Finance REST API v2.0.0"})

    return app

app = create_app()
