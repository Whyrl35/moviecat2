# from flasgger import swag_from
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from run import api
from .models import UserModel, RevokedTokenModel


parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class Registration(Resource):
    # @swag_from('./../docs/user_registration.yml')
    def post(self):

        if request.remote_addr != '127.0.0.1':
            return {'message': "Your are'nt authorized to access this route"}, 401

        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password'])
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


class Login(Resource):
    # @swag_from('./../docs/user_login.yml')
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 400

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 200, {'jwt-token': access_token}
        else:
            return {'message': 'Wrong credentials'}, 401


class LogoutAccess(Resource):
    @jwt_required
    # @swag_from('./../docs/user_logout_access.yml')
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    # @swag_from('./../docs/user_logout_refresh.yml')
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    # @swag_from('./../docs/token_refresh.yml')
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            return {'access_token': access_token}, 200, {'jwt-token': access_token}
        except:
            return {'message': 'Your not authorized.'}, 401


class DevToken(Resource):
    @jwt_refresh_token_required
    # @swag_from('./../docs/dev_token.yml')
    def post(self):
        if request.remote_addr != '127.0.0.1':
            return {'message': "Your are'nt authorized to access this route"}, 401

        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user, expires_delta=False)
            return {'access_token': access_token}
        except:
            return {'message': 'Your not authorized.'}, 401



class AllUsers(Resource):
    # @swag_from('./../docs/all_users.yml')
    def get(self):
        if request.remote_addr != '127.0.0.1':
            return {'message': "Your are'nt authorized to access this route"}, 401
        return UserModel.return_all()

    # @swag_from('./../docs/all_users.yml')
    def delete(self):
        if request.remote_addr != '127.0.0.1':
            return {'message': "Your are'nt authorized to access this route"}, 401
        return UserModel.delete_all()


#
# Adding resources:
api.add_resource(Registration, '/v1/private/registration')
api.add_resource(AllUsers, '/v1/private/users')
api.add_resource(DevToken, '/v1/private/devtoken')

api.add_resource(Login, '/v1/login')
api.add_resource(LogoutAccess, '/v1/logout/access')
api.add_resource(LogoutRefresh, '/v1/logout/refresh')
api.add_resource(TokenRefresh, '/v1/token/refresh')
