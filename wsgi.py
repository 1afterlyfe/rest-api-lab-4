from flask import Flask, jsonify
from flask_smorest import Api
from extensions import db, migrate, jwt
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from resources.users import blp as UsersBlueprint
from resources.categories import blp as CategoriesBlueprint
from resources.records import blp as RecordsBlueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py", silent=False)

    app.config["JWT_SECRET_KEY"] = "supersecret123"

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    api = Api(app)

    api.register_blueprint(UsersBlueprint)
    api.register_blueprint(CategoriesBlueprint)
    api.register_blueprint(RecordsBlueprint)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @app.route("/")
    def index():
        return jsonify({"message": "Finance REST API v2.0.0"})

    @app.route("/debug-key")
    def debug_key():
        return {"jwt_key": app.config["JWT_SECRET_KEY"]}

    @app.route("/whoami")
    @jwt_required()
    def whoami():
        return {"user_id": get_jwt_identity()}

    @app.route("/debug-decode", methods=["POST"])
    def debug_decode():
        data = request.get_json() or {}
        token = data.get("token", "")
        try:
            decoded = decode_token(token)
            return {"ok": True, "decoded": decoded}, 200
        except Exception as e:
            return {"ok": False, "error": str(e)}, 400

    return app


app = create_app()
