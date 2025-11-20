from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
from flask_jwt_extended import jwt_required

from extensions import db
from models import CategoryModel, UserModel
from schemas import CategorySchema, CategoryCreateSchema

blp = Blueprint(
    "Categories",
    "categories",
    description="Глобальні та користувацькі категорії витрат",
)

@blp.route("/categories")
class CategoriesList(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.order_by(CategoryModel.id).all()

    @jwt_required()
    @blp.arguments(CategoryCreateSchema)
    @blp.response(201, CategorySchema)
    def post(self, data):
        name = data["name"].strip()
        is_global = data.get("is_global", False)
        user_id = data.get("user_id")

        if not is_global:
            UserModel.query.get_or_404(user_id, description="Користувач не знайдений")


        existing = CategoryModel.query.filter_by(
            name=name,
            user_id=None if is_global else user_id
        ).first()
        if existing:
            scope = "глобальна" if is_global else "для цього користувача"
            abort(409, message=f"Категорія з такою назвою вже існує ({scope}).")

        category = CategoryModel(
            name=name,
            is_global=is_global,
            user_id=None if is_global else user_id,
        )
        db.session.add(category)
        db.session.commit()

        return category


@blp.route("/users/<int:user_id>/categories")
class UserVisibleCategories(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self, user_id):

        UserModel.query.get_or_404(user_id, description="Користувач не знайдений")

        categories = CategoryModel.query.filter(
            or_(
                CategoryModel.is_global.is_(True),
                CategoryModel.user_id == user_id,
            )
        ).order_by(CategoryModel.name).all()

        return categories

@blp.route("/categories/<int:category_id>")
class CategoryResource(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        return CategoryModel.query.get_or_404(
            category_id, description="Категорія не знайдена"
        )

    @jwt_required()
    @blp.response(204)
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(
            category_id, description="Категорія не знайдена"
        )
        db.session.delete(category)
        db.session.commit()
        return ""
