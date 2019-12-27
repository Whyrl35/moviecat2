from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from run import app, api
from .models import MovieModel, ActorModel, RealisatorModel


class Movies(Resource):
    # @swag_from('./../docs/movies_list.yml')
    def get(self, **kwargs):
        pass

    @jwt_required
    def post(self, id):
        pass

    @jwt_required
    def put(self, id):
        pass

    @jwt_required
    def delete(self, id):
        pass


class Movie(Resource):
    def get(self, id):
        pass

    @jwt_required
    def post(self, id):
        pass

    @jwt_required
    def put(self, id):
        pass

    @jwt_required
    def delete(self, id):
        pass





