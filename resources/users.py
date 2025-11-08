from flask.views import MethodView
from flask_smorest import Blueprint, abort

from extensions import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint(
    "Users",
    "users",
    description="Операції з користувачами",
)

@blp.route("/users")
class UsersList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter_by(username=user_data["username"]).first():
            abort(409, message="Користувач з таким username вже існує.")
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/users/<int:user_id>")
class UserResource(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(
            user_id, description="Користувача не знайдено"
        )

    @blp.response(204)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(
            user_id, description="Користувача не знайдено"
        )
        db.session.delete(user)
        db.session.commit()
        return ""
