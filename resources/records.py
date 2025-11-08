from flask.views import MethodView
from flask_smorest import Blueprint, abort
from extensions import db
from models import RecordModel, UserModel, CategoryModel
from schemas import RecordSchema

blp = Blueprint(
    "Records",
    "records",
    description="Операції з витратами",
)


@blp.route("/records")
class RecordsList(MethodView):
    @blp.response(200, RecordSchema(many=True))
    def get(self):
        return RecordModel.query.order_by(RecordModel.id).all()

    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(self, data):
        user = UserModel.query.get_or_404(
            data["user_id"], description="Користувач не знайдений"
        )
        category = CategoryModel.query.get_or_404(
            data["category_id"], description="Категорія не знайдена"
        )

        if not (category.is_global or category.user_id == user.id):
            abort(400, message="Користувач не може використовувати цю категорію.")

        record = RecordModel(
            user_id=user.id,
            category_id=category.id,
            amount=data["amount"],
            description=data.get("description"),
        )
        db.session.add(record)
        db.session.commit()
        return record
