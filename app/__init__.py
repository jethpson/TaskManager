import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Paths
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Load configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "users.login_page"  # frontend login page

    # Handle unauthorized access
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for("users.login_page"))

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500

    # Import models after db is initialized
    from app.models import User, Task

    # Import and register blueprints
    from app.routes import users_bp
    from app.tasks_routes import tasks_bp

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    # Redirect root URL to dashboard
    @app.route('/')
    def home_redirect():
        if current_user.is_authenticated:
            return redirect(url_for('users.dashboard'))  # go to dashboard
        else:
            return redirect(url_for('users.login_page'))  # go to login

    return app

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
