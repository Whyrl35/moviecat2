from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from run import app, api
from .models import Movie, Actor, Realisator


class Movies(Resource):
    # @swag_from('./../docs/movies_list.yml')
    def get(self):
        pass

class MovieAdd(Resource):
    def post(self, title):
        pass