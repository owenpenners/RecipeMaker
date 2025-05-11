from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Recipe model with a user_id
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Rating and Comment models
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


@app.route('/')
@login_required
def index():
    # user_id = session.get('user_id', 1)  # TEMP user_id placeholder
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', recipes=recipes)



@app.route('/recipe/<int:id>', methods=['GET', 'POST'])
def view_recipe(id):
    from forms import RatingForm, CommentForm
    recipe = Recipe.query.get_or_404(id)
    rating_form = RatingForm()
    comment_form = CommentForm()

    if rating_form.validate_on_submit() and 'value' in request.form and current_user.is_authenticated:
        existing = Rating.query.filter_by(user_id=current_user.id, recipe_id=id).first()
        if existing:
            existing.value = rating_form.value.data
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


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        user_id = current_user.id  #  user_id
        new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, user_id=user_id)
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == 'POST':
        recipe.ingredients = request.form['ingredients']
        recipe.instructions = request.form['instructions']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', recipe=recipe)

@app.route('/delete/<int:id>')
@login_required
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('index'))


# Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Logged in successfully.")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.")
    return render_template("login.html", form=form)

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for('index'))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash pass hopefully
        hashed = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
