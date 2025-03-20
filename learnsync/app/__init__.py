from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.routes.dashboard import dashboard as dashboard_bp
    app.register_blueprint(dashboard_bp)
    
    from app.routes.groups import groups as groups_bp
    app.register_blueprint(groups_bp)
    
    from app.routes.materials import materials as materials_bp
    app.register_blueprint(materials_bp)
    
    from app.routes.chats import chats as chats_bp
    app.register_blueprint(chats_bp)
    
    from app.routes.schedule import schedule as schedule_bp
    app.register_blueprint(schedule_bp)
    
    from app.routes.ai import ai as ai_bp
    app.register_blueprint(ai_bp)
    
    return app
