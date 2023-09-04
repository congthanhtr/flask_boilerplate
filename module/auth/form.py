from flask import flash
from sqlalchemy import or_
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from .model import User
from .validators import (
    CommonPassword, NumericPassword, UserAttributeSimilarity, ValidatePassword)
from werkzeug.security import generate_password_hash


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=8, max=64),
                                CommonPassword(), NumericPassword(),
                                UserAttributeSimilarity(), ValidatePassword()])
    password2 = PasswordField(
        'Password confirmation',
        validators=[DataRequired(), EqualTo('password')])

    def validate(self):
        user = User.query.filter(
            or_(User.username == self.username.data,
                User.email == self.email.data)).first()
        if user is not None:
            flash('This username or email is already taken. '
                  'Please choose a different one.')
            return False

        return True

    def validate_password(self, password):
        # temporary user instance
        _user = User(
            email=self.email.data,
            password=generate_password_hash(self.password.data))

        # UserAttributeSimilarity
        # the password is sufficiently different from the user's attributes.
        self.password.validators[-2](self, password, _user)
