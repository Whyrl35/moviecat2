from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from run import app, api
from .models import RealisatorModel


class Realisators(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, action='append', required=False, help="List of realisator's id")
        args = parser.parse_args()

        if args.id:
            realisators_list = list()
            for id in args.id:
                realisators_list.append(RealisatorModel.find_by_id(id))
            realisators = {'realisators': realisators_list}
        else:
            realisators = {'realisators': RealisatorModel.return_all()}

        return {
            "data": realisators,
            "message": "Successfuly returning the realisator list",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
        }, 200

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('realisators', type=list, location='json', required=True, help="Missing the realisator's list")
        args = parser.parse_args()
        realisators_list = list()

        for realisator in args.realisators:
            found_realisator = RealisatorModel.find_by_name(realisator['first_name'], realisator['last_name'])
            if found_realisator:
                realisators_list.append(found_realisator)
            else:
                new_realisator = RealisatorModel()
                new_realisator.first_name = realisator['first_name']
                new_realisator.last_name = realisator['last_name']
                new_realisator.save_to_db()
                realisators_list.append(RealisatorModel.to_json(new_realisator))

        realisators = {'realisators': realisators_list}
        return {
            "data": realisators,
            "message": "Successfuly adding the realisator list",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
        }, 201

    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, action='append', required=True, help="Missing list of realisator's id")
        args = parser.parse_args()

        realisators_list = list()
        for id in args.id:
            realisator = RealisatorModel.find_by_id(id)
            if realisator:
                RealisatorModel.delete_by_id(id)
                realisators_list.append(realisator)

        realisators = {'realisators': realisators_list}
        return {
            "data": realisators,
            "message": "Successfuly deleting the realisator list",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
        }, 201


class Realisator(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="Missing the id of the realisator")
        args = parser.parse_args()

        try:
            realisator = RealisatorModel.find_by_id(args.id)
        except AttributeError:
            return {
                "data": None,
                "error": "realisator with this id doesn't exist",
                "file": __name__,
                "cls": self.__class__.__name__,
                "args": args
                }, 404
        except:
            return {
                "data": None,
                "error": "Error during execution",
                "file": __name__,
                "cls": self.__class__.__name__,
                "args": args
                }, 500

        return {
            "data": { 'realisator': realisator },
            "message": "Successfuly fetching realisator",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
            }, 200

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True, help="Missing the first name of the realisator")
        parser.add_argument('last_name', type=str, required=True, help="Missing the last name of the realisator")
        args = parser.parse_args()

        realisator = RealisatorModel.find_by_name(args.first_name, args.last_name)
        if realisator:
            return {
                "data": {'realisator': realisator},
                "message": "realisator already exists",
                "file": __name__,
                "cls": self.__class__.__name__,
                "args": args
                }, 200

        try:
            realisator = RealisatorModel()
            realisator.first_name = args.first_name
            realisator.last_name = args.last_name
            realisator.save_to_db()
        except:
            return {
                "data": None,
                "error": "Error during realisator creation",
                "file": __name__,
                "cls": self.__class__.__name__,
                "args": args
                }, 500

        return {
            "data": {'realisator': RealisatorModel.to_json(realisator)},
            "message": "Successfuly adding the realisator",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
            }, 201

    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="Missing the ID of the realisator")
        args = parser.parse_args()

        try:
            RealisatorModel.delete_by_id(args.id)
        except:
            return {
                "data": None,
                "error": "Error during realisator deletion, or it don't exists",
                "file": __name__,
                "cls": self.__class__.__name__,
                "args": args
                }, 404

        return {
            "data": None,
            "message": "Successfuly deleting the realisator",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
            }, 200


#
# Adding resources:
api.add_resource(Realisators, '/v1/realisators')
api.add_resource(Realisator, '/v1/realisator')