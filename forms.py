from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

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


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email    = StringField('Email',    validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[Optional(), Length(min=8)])
    confirm  = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit   = SubmitField('Update Profile')

class RecipeForm(FlaskForm):
    title        = StringField('Title', validators=[DataRequired()])
    ingredients  = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    tags         = StringField('Tags (comma-separated)', validators=[Optional()])
    submit       = SubmitField('Save')