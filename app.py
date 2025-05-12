from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm, ProfileForm, RecipeForm
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),   primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

recipe_tags = db.Table('recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('tag_id',    db.Integer, db.ForeignKey('tag.id'),    primary_key=True)
)

# Tags for recipes model
class Tag(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')
    favorites = db.relationship('Recipe', secondary=favorites, backref=db.backref('saved_by', lazy='dynamic'), lazy = 'dynamic')


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
    tags = db.relationship('Tag', secondary=recipe_tags, backref=db.backref('recipes', lazy='dynamic'), lazy='dynamic')

# makes database
# with app.app_context():
 #   db.create_all()

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
    form = RecipeForm()
    if form.validate_on_submit():
        r = Recipe(
            title        = form.title.data,
            ingredients  = form.ingredients.data,
            instructions = form.instructions.data,
            author       = current_user
        )
        # attach tags
        names = {t.strip().lower() for t in form.tags.data.split(',') if t.strip()}
        for name in names:
            tag = Tag.query.filter_by(name=name).first() or Tag(name=name)
            r.tags.append(tag)

        db.session.add(r)
        db.session.commit()
        flash('Recipe created!')
        return redirect(url_for('index'))

    return render_template('create.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    form   = RecipeForm(obj=recipe)
    if form.validate_on_submit():
        recipe.title        = form.title.data
        recipe.ingredients  = form.ingredients.data
        recipe.instructions = form.instructions.data

        # attach tags
        recipe.tags = []
        names = {t.strip().lower() for t in form.tags.data.split(',') if t.strip()}
        for name in names:
            tag = Tag.query.filter_by(name=name).first() or Tag(name=name)
            recipe.tags.append(tag)

        db.session.commit()
        flash('Recipe updated!')
        return redirect(url_for('index'))

    # populate tags
    form.tags.data = ', '.join(t.name for t in recipe.tags)
    return render_template('edit.html', form=form, recipe=recipe)

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
        # hashed = generate_password_hash(form.password.data)
        hashed = generate_password_hash( form.password.data, method='pbkdf2:sha256' )
        new_user = User( username=form.username.data, email=form.email.data, password=hashed )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# view profile
@app.route('/profile')
@login_required
def profile():
    # shows user, recipes, & favorites maybe
    return render_template('profile.html', user=current_user, recipes=current_user.recipes,favorites=current_user.favorites.all())

# edit profile, edit's username email and pass
@app.route('/profile/edit', methods=['GET','POST'])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email    = form.email.data
        if form.password.data:
           current_user.password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
           


        db.session.commit()
        flash('Profile updated.')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', form=form)

# searches for recipes
@app.route('/search', methods=['GET'])
@login_required
def search_recipes():
    q       = request.args.get('q', '').strip()
    tag_name = request.args.get('tag', '').strip().lower()

    # shows all recipes
    base = Recipe.query

    # if search term is typed
    if q:
        base = base.filter(Recipe.title.ilike(f'%{q}%'))

    # clicked tag filter
    if tag_name:
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag:
            # only recipes having that tag
            base = base.join(Recipe.tags).filter(Tag.id == tag.id)
        else:
            base = base.filter(False)  # no such tag → empty

    results  = base.all()
    all_tags = Tag.query.order_by(Tag.name).all()

    return render_template('search.html', results=results, q=q, all_tags=all_tags, current_tag=tag_name)

# save to fave
@app.route('/favorite/<int:id>', methods=['POST'])
@login_required
def favorite(id):
    recipe = Recipe.query.get_or_404(id)
    if not current_user.favorites.filter_by(id=recipe.id).first():
        current_user.favorites.append(recipe)
        db.session.commit()
        flash('Recipe Saved!')
    else:
        flash('Already in favorites.')
    return redirect(request.referrer or url_for('view_recipe', id=id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
