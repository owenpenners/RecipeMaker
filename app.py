
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm, RatingForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/recipe/<int:id>', methods=['GET', 'POST'])
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    rating_form = RatingForm()
    comment_form = CommentForm()

    if rating_form.validate_on_submit() and 'value' in request.form and current_user.is_authenticated:
        existing_rating = Rating.query.filter_by(user_id=current_user.id, recipe_id=id).first()
        if existing_rating:
            existing_rating.value = rating_form.value.data
        else:
            db.session.add(Rating(value=rating_form.value.data, user_id=current_user.id, recipe_id=id))
        db.session.commit()
        flash("Rating submitted.")
        return redirect(url_for('view_recipe', id=id))

    if comment_form.validate_on_submit() and 'text' in request.form and current_user.is_authenticated:
        db.session.add(Comment(text=comment_form.text.data, user_id=current_user.id, recipe_id=id))
        db.session.commit()
        flash("Comment added.")
        return redirect(url_for('view_recipe', id=id))

    ratings = Rating.query.filter_by(recipe_id=id).all()
    avg_rating = round(sum(r.value for r in ratings) / len(ratings), 1) if ratings else "No ratings yet"
    comments = Comment.query.filter_by(recipe_id=id).all()

    return render_template('view.html', recipe=recipe, rating_form=rating_form,
                           comment_form=comment_form, avg_rating=avg_rating, comments=comments)
