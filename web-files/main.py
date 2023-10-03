from website import create_app, db
from flask_migrate import Migrate


migrate = Migrate()



app = create_app(migrate)




#Mail Verification Section




#if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')