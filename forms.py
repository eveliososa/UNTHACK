from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length, EqualTo)

from models import User


# FUNCTION TO TEST IF EMAIL AND USERNAME ARE UNIQUE
def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


def username_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that username already exists.')


# FORM FOR SIGN UP
class SignUpForm(FlaskForm):
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z]'
            )
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z]'
            )
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            username_exists
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match')
        ]
    )
    password2 = PasswordField(
        'Confirm password',
        validators=[
            DataRequired()
        ]
    )


# LOG IN FORM
class LogInForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )


# FLIGHT SEARCH FORM
class FlightSearchForm(FlaskForm):
    date = StringField(
        'Date',
        validators=[
            DataRequired()
        ]
    )
    origin = StringField(
        'From',
        validators=[
            DataRequired()
        ]
    )
    destination = StringField(
        'To',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Search')


# UPDATE FLIGHT SEAT
class UpdateSeatForm(FlaskForm):
    new_seat = StringField("Selected Seat")
    submit = SubmitField("Save Changes")
