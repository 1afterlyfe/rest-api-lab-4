from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1, max=128))

class UserRegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=128))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))

class UserLoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1, max=128))
    password = fields.Str(required=True, load_only=True)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=128))
    is_global = fields.Bool(required=True)
    user_id = fields.Int(allow_none=True, dump_only=True)


class CategoryCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=128))
    is_global = fields.Bool(load_default=False)
    user_id = fields.Int(load_default=None, allow_none=True)

    @validates_schema
    def validate_scope(self, data, **kwargs):
        is_global = data.get("is_global", False)
        user_id = data.get("user_id")

        if is_global and user_id:
            raise ValidationError(
                "Глобальна категорія не може мати user_id.",
                field_name="user_id",
            )

        if not is_global and not user_id:
            raise ValidationError(
                "Для користувацької категорії потрібно вказати user_id.",
                field_name="user_id",
            )


class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    description = fields.Str(load_default=None)
    created_at = fields.DateTime(dump_only=True)
