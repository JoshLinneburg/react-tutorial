from flask_app import ma
from flask_app.models import User, Role, UserRole


# class RoleSchema(ma.Schema):
#     class Meta:
#         model = UserRole
#
#         fields = tuple(
#             "user_id",
#         )


class UserSchema(ma.Schema):
    class Meta:
        model = User

        fields = (
            "public_id",
            "first_name",
            "middle_name",
            "last_name",
            "profile_picture_url",
            "email",
            "phone_nbr",
            "gender",
            "date_of_birth",
            "employ_status",
            "housing_status",
            # "head_of_household_id",
            # "household_members",
            "addr_1",
            "addr_2",
            "addr_city",
            "addr_state",
            "addr_postal_cd",
            # "roles",
            "_links",
        )

        ordered = True

    # roles = ma.Nested("RoleSchema", many=True)

    _links = ma.Hyperlinks(
        {
            "self": {
                "href": ma.URLFor(
                    "users_bp.read_single_user",
                    public_user_id="<public_id>",
                    _external=True,
                )
            },
            # "collection": {"href": ma.URLFor("users_bp.read_users", _external=True)},
        }
    )
