from flask import Flask
# from flasgger import Swagger, LazyJSONEncoder
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import yaml

with open("conf.yml", 'r') as config_file:
    configuration = yaml.load(config_file, Loader=yaml.FullLoader)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'some-secret-string'
# app.config['YAML'] = configuration
app.config['JWT_SECRET_KEY'] = configuration['jwt_secret_key']
app.config['JWT_AUTH_URL_RULE'] = '/api/auth'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


import resources
from resources import *


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return resources.models.RevokedTokenModel.is_jti_blacklisted(jti)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
