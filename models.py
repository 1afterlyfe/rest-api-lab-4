from datetime import datetime
from extensions import db


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)

    records = db.relationship(
        "RecordModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    categories = db.relationship(
        "CategoryModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    is_global = db.Column(db.Boolean, default=False, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    user = db.relationship("UserModel", back_populates="categories")
    records = db.relationship("RecordModel", back_populates="category")

    __table_args__ = (
        db.UniqueConstraint("name", "user_id", name="uq_category_name_user"),
    )


class RecordModel(db.Model):
    __tablename__ = "record"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    user = db.relationship("UserModel", back_populates="records")
    category = db.relationship("CategoryModel", back_populates="records")
