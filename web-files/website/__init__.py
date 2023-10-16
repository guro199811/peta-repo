from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()

mail = Mail()




def create_app(migrate):
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.config['SECRET_KEY'] = 'uwdhujiwakopdwu9faoijskpdwuahpfoijasidowiano'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@postgres:5432/petsite'
    # app.config['SERVER_NAME'] = 'localhost:8000'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    app.config.from_pyfile('mail_config.cfg')
    
    
    #rest of the app
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        mail.init_app(app)

    from .views import views
    from .auth import auth
    from .general_logic import general_logic

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(general_logic, url_prefix="/")

    # ვეუბნებით ფლასკს როგორ ჩავტვირთოთ მომხმარებელი (Primary key)-ით
    from .models import Person

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Person.query.get(int(id))
    

    return app
