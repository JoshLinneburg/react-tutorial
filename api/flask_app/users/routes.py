import uuid
from datetime import datetime
from flask import Blueprint, request, current_app, render_template, make_response
from flask_app import db
from flask_app.models import User
from flask_app.schemas import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, decode_token
from jwt.exceptions import DecodeError
from sqlalchemy import or_
from pprint import pprint
from werkzeug.security import generate_password_hash

users_bp = Blueprint("users_bp", __name__, url_prefix="/api/v1/user")


@users_bp.route("", methods=["GET"])
@jwt_required()
def read_users():
    headers = request.headers
    access_token = headers.get("Authorization").split(" ")[-1]

    try:
        decoded_token = decode_token(encoded_token=access_token)
        pprint(decoded_token)
    except DecodeError:
        return make_response({"message": "Could not decode access token"}, 422)

    users = User.query.all()
    user_schema = UserSchema(many=True)
    user_data = user_schema.dump(users)

    return make_response({"body": user_data}, 200)
    

@users_bp.route("/<public_user_id>", methods=["GET"])
def read_single_user(public_user_id):
    user = User.query.filter_by(public_id=public_user_id).first()

    if not user:
        return make_response({"message": "User not found!"}, 404)

    user_schema = UserSchema()
    user_data = user_schema.dump(user)

    return make_response({"body": user_data}, 200)


@users_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json()
    password_hash = generate_password_hash(password=data.get("password"), method="sha256")
    user = User.query.filter(
        or_(User.email == data.get("email", "invalid"), User.phone_nbr == data.get("phone_nbr", "invalid"))
    ).first()

    if user:
        return make_response(
            {
                "message": "User already exists with that email or phone number!"
            }, 400
        )

    user = User(
        public_id=str(uuid.uuid4()),
        first_name=data["first_name"],
        middle_name=data.get("middle_name", None),
        last_name=data["last_name"],
        email=data.get("email", None),
        phone_nbr=data.get("phone_nbr", None),
        password_hash=password_hash,
        user_confirmed_ind=False,
        gender=data.get("gender"),
        date_of_birth=datetime.strptime(data.get("date_of_birth"), "%Y-%m-%d") if data.get("date_of_birth") else None,
        employment_status=data.get("employment_status", None),
        housing_status=data.get("housing_status", None),
        addr_1=data.get("addr_1"),
        addr_2=data.get("addr_2", None),
        addr_city=data.get("addr_city"),
        addr_state=data.get("addr_state"),
        addr_postal_cd=data.get("addr_postal_cd"),
    )

    db.session.add(user)
    db.session.commit()
    user_schema = UserSchema()
    user_data = user_schema.dump(user)

    return make_response(
        {
            "body": user_data,
            "message": "User created!"
        }, 201
    )


@users_bp.route("/<public_user_id>", methods=["PATCH"])
def update_user(public_user_id):
    data = request.get_json()

    immutable_fields = [
        "id",
        "public_id",
        "created_datetime",
        "modified_datetime",
    ]

    user = User.query.filter_by(public_id=public_user_id).first()

    if not user:
        return make_response(
            {
                "body": {"message": "User not found!"}
            }, 404
        )
    # elif public_user_id != get_jwt_identity():
    #     return {"status": "NOT OK!", "status_code": 403, "body": {"message": "You can't update another user's data!"}}

    print(data)

    for key, value in data.items():
        if key in immutable_fields:
            continue
        elif key == "password":
            user.set_password(password=data["password"])
        else:
            setattr(user, key, value)

    db.session.commit()

    user_schema = UserSchema()
    user_data = user_schema.dump(user)

    return make_response(
        {
            "body": user_data
        }, 200
    )


@users_bp.route("/<public_user_id>", methods=["DELETE"])
def delete_user(public_user_id):
    user = User.query.filter_by(public_id=public_user_id).first()

    if not user:
        return make_response(
            {
                "body": {"message": "User not found!"}
            }, 404
        )

    db.session.delete(user)
    db.session.commit()

    return make_response(
        {
            "body": {"message": "User deleted!"}
        }, 200
    )
