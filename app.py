import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
## SQLAlchemy will help to create table from below import statement
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


db_url = os.environ.get('DATABASE_URL', 'sqlite:///data.db') # Cloud: postgres, local: sqlite
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app=app,
          authentication_handler=authenticate,
          identity_handler=identity)    # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            print('Created Table')
            db.create_all()

    app.run(port=5000)


