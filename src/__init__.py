import os, click
from flask import Flask, request, session, g, render_template, redirect, url_for, abort, flash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, dotenv_values
from config import config
import sqlalchemy as sa
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf_protection = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name='development'):
    app = Flask(__name__)
    load_dotenv('.env')
    # environment_configuration = os.environ['CONFIGURATION_SETUP']
    # app.config.from_object(environment_configuration)
    # app.config.from_mapping(
    #     DATABASE_URL= os.path.join(app.instance_path, 'app.db')    
    # )
    app.config.from_object(config[config_name])
    # config[config_name].init_app(app)
    app.config.from_pyfile("../config.py")
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    initialize_extensions(app)
    register_blueprints(app)
    register_cli_commands(app)
    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("user"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')

    ########################
    #### error handlers ####
    ########################


    @app.errorhandler(401)
    def unauthorized_page(error):
        return render_template("errors/401.html"), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template("errors/405.html"), 405

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/500.html"), 500
    
    return app

# ----------------
# Helper Functions
# ----------------

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)
    csrf_protection.init_app(app)
    login_manager.init_app(app)

    from src.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

def register_blueprints(app):
    # register blueprints here
    from src.post import post_bp
    app.register_blueprint(post_bp)
    from src.auth import auth_bp
    app.register_blueprint(auth_bp)

def register_cli_commands(app):
    @app.cli.command('init_db')
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        click.echo('Database initialized')
