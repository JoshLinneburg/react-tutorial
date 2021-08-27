from datetime import datetime
from flask_app import db
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash


UserRole = db.Table(
    'user_role',
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True)
)


class User(db.Model):
    id = Column(Integer, primary_key=True)
    public_id = Column(String(128), unique=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=False)
    profile_picture_url = db.Column(String(128))

    email = Column(String(50))
    phone_nbr = Column(String(15))
    password_hash = db.Column(db.String(128))
    user_confirmed_ind = db.Column(Boolean, nullable=False)

    gender = Column(String(15))
    date_of_birth = Column(Date)
    employment_status = Column(String(50))
    housing_status = Column(String(50))
    head_of_household_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    household_members = relationship("User", backref=db.backref("head_of_household", remote_side=[id]), lazy="dynamic",
                                     passive_deletes=True)

    addr_1 = Column(String(128))
    addr_2 = Column(String(128))
    addr_city = Column(String(128))
    addr_state = Column(String(2))
    addr_postal_cd = Column(Integer)

    roles = relationship("Role", secondary=UserRole, backref="users")

    created_datetime = Column(DateTime, default=datetime.utcnow)
    modified_datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"User {self.public_id}"

    def __str__(self):
        string_to_return = " ".join(
            [
                self.first_name.capitalize(),
                self.last_name.capitalize() + ",",
                "born on:",
                str(self.date_of_birth),
            ]
        )
        return string_to_return

    def set_password(self, password):
        """
        Sets the password of the User to the password passed in.
        Args:
            password: str
                A str containing the User's new password.
        Returns:
            None.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks the hash of a User's password against the hash of a password they've
        provided for authentication.
        Args:
            password: str
                A str containing the password the User wants to authenticate with.
        Returns:
            result: bool
                Whether the password the User provided matches the
                password associated with their account.
        """
        result = check_password_hash(self.password_hash, password)
        return result


class Role(db.Model):
    id = Column(Integer, primary_key=True)
    public_id = Column(String(128), unique=True)
    role_name = Column(String(25), nullable=False)
    created_datetime = Column(DateTime, default=datetime.utcnow)
    modified_datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Go with the Table instead of the Class if there's no other fields to track...
# class UserRole(db.Model):
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
#     role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=True, primary_key=True)

