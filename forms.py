from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username     = StringField('Username', validators=[DataRequired()])
    password     = PasswordField('Password', validators=[DataRequired()])
    remember_me  = BooleanField('Remember me')
    submit       = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email    = StringField('Email',    validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm  = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit   = SubmitField('Register')


from wtforms import IntegerField, TextAreaField
from wtforms.validators import NumberRange

class RatingForm(FlaskForm):
    value = IntegerField('Rating (1–5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Rating')

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')
