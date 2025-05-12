from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, NumberRange

class LoginForm(FlaskForm):
    username     = StringField('Username', validators=[DataRequired()])
    password     = PasswordField('Password', validators=[DataRequired()])
    remember_me  = BooleanField('Remember me')
    submit       = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email    = StringField('Email',    validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm  = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit   = SubmitField('Register')

class RatingForm(FlaskForm):
    value = IntegerField('Rating (1–5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Rating')

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email    = StringField('Email',    validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[Optional()])
    confirm  = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit   = SubmitField('Update Profile')

class RecipeForm(FlaskForm):
    title        = StringField('Title', validators=[DataRequired()])
    ingredients  = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    tags         = StringField('Tags (comma-separated)', validators=[Optional()])
    submit       = SubmitField('Save')
