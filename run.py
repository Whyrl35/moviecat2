from flask import Flask
# from flasgger import Swagger, LazyJSONEncoder
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import yaml

with open("conf.yml", 'r') as config_file:
    configuration = yaml.load(config_file)
