from flask import Flask, g
from flask_login import LoginManager
import logging
from database import get_db, engine, Base
import views, models


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
login_manager = LoginManager()

db_url = engine.url
secret_key = 'supersecretkey'

def create_app():
    Base.metadata.create_all(bind=engine)

    app = Flask(__name__)
    app.secret_key = secret_key
    app.debug = True
    login_manager.init_app(app)

    for module in views.blueprints:
        app.register_blueprint(module)

    @app.teardown_appcontext
    def remove_session(exception=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    if not app.debug:
        file_handler = logging.FileHandler('flask.log')
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)
    return app


@login_manager.user_loader
def load_user(user_id):
    try:
        with get_db() as db:
            return db.query(models.User).filter_by(id=user_id).first()
    except:
        return None


if __name__ == '__main__':
    app = create_app()
    app.run()