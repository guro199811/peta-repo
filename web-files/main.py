from website import create_app, db
from flask_migrate import Migrate
import os



migrate = Migrate()



app = create_app(migrate)




#Mail Verification Section


# Check if the PORT environment variable is set (for Heroku)
'''if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)'''