from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required
from passlib.hash import pbkdf2_sha256

from extensions import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema, UserLoginSchema

blp = Blueprint(
    "Users",
    "users",
    description="Операції з користувачами та автентифікація",
)


@blp.route("/users")
class UsersList(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter_by(username=user_data["username"]).first():
            abort(400, message="Користувач з таким username вже існує.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/users/<int:user_id>")
class UserResource(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(
            user_id, description="Користувача не знайдено"
        )

    @jwt_required()
    @blp.response(204)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(
            user_id, description="Користувача не знайдено"
        )
        db.session.delete(user)
        db.session.commit()
        return ""


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(username=user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200

        abort(401, message="Невірний логін або пароль.")
