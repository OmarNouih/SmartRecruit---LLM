from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate # type: ignore
from pymongo import MongoClient
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
sess = Session()

mongo_client = MongoClient('mongodb://localhost:27017/')
mongodb = mongo_client['applications']
applications_collection = mongodb['applications']

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)  
    migrate.init_app(app, db)
    sess.init_app(app)

    with app.app_context():
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        return app
