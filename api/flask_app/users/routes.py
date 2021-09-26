import logging
import os
import uuid
from datetime import datetime
from flask import Blueprint, request, make_response
from flask_app import db
from flask.helpers import Response
from flask_app.models import User
from flask_app.schemas import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from fusionauth.fusionauth_client import FusionAuthClient
from sqlalchemy import or_
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from werkzeug.security import generate_password_hash

users_bp = Blueprint("users_bp", __name__, url_prefix="/api/v1/user")
fusionauth_client = FusionAuthClient(os.environ.get("FUSIONAUTH_API_KEY"), os.environ.get("FUSIONAUTH_BASE_URL"))


@users_bp.route("", methods=["GET"])
@jwt_required()
def read_users() -> Response:
    users = User.query.all()
    user_schema = UserSchema(many=True)
    user_data = user_schema.dump(users)
    return make_response({"body": user_data, "message": "User retrieved."}, 200)


@users_bp.route("/<str:public_user_id>", methods=["GET"])
def read_single_user(public_user_id: str) -> Response:
    try:
        user = User.query.filter_by(public_id=public_user_id).one()
        user_schema = UserSchema()
        user_data = user_schema.dump(user)
        return make_response({"body": user_data}, 200)

    except NoResultFound:
        return make_response({"body": None, "message": "User not found."}, 404)

    except Exception as e:
        logging.exception(e)
        return make_response({"body": None, "message": e}, 400)


@users_bp.route("", methods=["POST"])
def create_user():
    try:

        data = request.get_json()
        user = User.query.filter(
            or_(User.email == data.get("email", "invalid"), User.phone_nbr == data.get("phone_nbr", "invalid"))
        ).first()

        if user:
            return make_response({"body": None, "message": "User already exists with that email or phone number."}, 400)

        user = User(
            public_id=str(uuid.uuid4()),
            first_name=data["first_name"],
            middle_name=data.get("middle_name"),
            last_name=data["last_name"],
            email=data.get("email"),
            phone_nbr=data.get("phone_nbr"),
            password_hash=generate_password_hash(password=data.get("password"), method="sha256"),
            user_confirmed_ind=False,
            gender=data.get("gender"),
            date_of_birth=datetime.strptime(data.get("date_of_birth"), "%Y-%m-%d")
            if data.get("date_of_birth")
            else None,
            employment_status=data.get("employment_status"),
            housing_status=data.get("housing_status"),
            addr_1=data.get("addr_1"),
            addr_2=data.get("addr_2"),
            addr_city=data.get("addr_city"),
            addr_state=data.get("addr_state"),
            addr_postal_cd=data.get("addr_postal_cd"),
        )

        # Add record to DB
        db.session.add(user)

        user_request = {
            "skipVerification": True,
            "user": {
                "firstName": user.first_name,
                "lastName": user.last_name,
                "birthDate": user.date_of_birth,
                "email": user.email,
                "mobilePhone": user.phone_nbr,
                "password": data.get("password"),
            },
        }

        # Add record to FusionAuth
        client_response = fusionauth_client.create_user(request=user_request, user_id=user.public_id)
        if client_response.was_successful():
            print(client_response.success_response)
        else:
            return make_response({"body": None, "message": client_response.error_response}, 400)

        db.session.commit()
        user_schema = UserSchema()
        user_data = user_schema.dump(user)

        return make_response({"body": user_data, "message": "User created."}, 201)

    except Exception as e:
        db.session.rollback()
        logging.exception(e)
        return make_response({"body": None, "message": e}, 400)


@users_bp.route("/<str:public_user_id>", methods=["PATCH"])
@jwt_required()
def update_user(public_user_id) -> Response:
    try:
        if (public_user_id != get_jwt_identity()) and ("admin" not in get_jwt()["roles"]):
            return make_response(
                {"body": None, "message": "You can't update another user's data without admin privileges."}, 403
            )

        data = request.get_json()

        immutable_fields = ["id", "public_id", "created_datetime", "modified_datetime"]

        user = User.query.filter_by(public_id=public_user_id).first()

        if not user:
            return make_response({"body": None, "message": "User not found."}, 404)

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

        return make_response({"body": user_data, "message": "User updated."}, 200)

    except Exception as e:
        db.session.rollback()
        logging.exception(e)
        return make_response({"body": None, "message": e}, 400)


@users_bp.route("/<str:public_user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(public_user_id) -> Response:
    try:
        if (public_user_id != get_jwt_identity()) and ("admin" not in get_jwt()["roles"]):
            return make_response(
                {"body": None, "message": "You can't delete another user without admin privileges."}, 403
            )
        user = User.query.filter_by(public_id=public_user_id).first()

        if not user:
            return make_response({"body": None, "message": "User not found."}, 404)

        db.session.delete(user)
        db.session.commit()

        return make_response({"body": None, "message": "User deleted."}, 200)

    except Exception as e:
        db.session.rollback()
        logging.exception(e)
        return make_response({"body": None, "message": e}, 400)
