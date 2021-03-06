from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from run import app, api
from .models import ActorModel


class Actors(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, action='append', required=False, help="List of actor's id")
        args = parser.parse_args()

        if args.id:
            actors_list = list()
            for id in args.id:
                actors_list.append(ActorModel.find_by_id(id))
            actors = {'actors': actors_list}
        else:
            actors = {'actors': ActorModel.return_all()}

        return {
            "data": actors,
            "message": "Successfuly returning the actor list",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
        }, 200

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('actors', type=list, location='json', required=True, help="Missing the actor's list")
        args = parser.parse_args()
        actors_list = list()

        for actor in args.actors:
            found_actor = ActorModel.find_by_name(actor['first_name'], actor['last_name'])
            if found_actor:
                actors_list.append(found_actor)
            else:
                new_actor = ActorModel()
                new_actor.first_name = actor['first_name']
                new_actor.last_name = actor['last_name']
                new_actor.save_to_db()
                actors_list.append(ActorModel.to_json(new_actor))

        actors = {'actors': actors_list}
        return {
            "data": actors,
            "message": "Successfuly adding the actor list",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
        }, 201

    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, action='append', required=True, help="Missing list of actor's id")
        args = parser.parse_args()

        actors_list = list()
        for id in args.id:
            actor = ActorModel.find_by_id(id)
            if actor:
                ActorModel.delete_by_id(id)
                actors_list.append(actor)

        actors = {'actors': actors_list}
        return {
            "data": actors,
            "message": "Successfuly deleting the actor list",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
        }, 201


class Actor(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="Missing the id of the actor")
        args = parser.parse_args()

        try:
            actor = ActorModel.find_by_id(args.id)
        except AttributeError:
            return {
                "data": None,
                "error": "Actor with this id doesn't exist",
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
            "data": { 'actor': actor },
            "message": "Successfuly fetching actor",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
            }, 200

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True, help="Missing the first name of the actor")
        parser.add_argument('last_name', type=str, required=True, help="Missing the last name of the actor")
        args = parser.parse_args()

        actor = ActorModel.find_by_name(args.first_name, args.last_name)
        if actor:
            return {
                "data": {'actor': actor},
                "message": "Actor already exists",
                "file": __name__,
                "cls": self.__class__.__name__,
                "args": args
                }, 200

        try:
            actor = ActorModel()
            actor.first_name = args.first_name
            actor.last_name = args.last_name
            actor.save_to_db()
        except:
            return {
                "data": None,
                "error": "Error during actor creation",
                "file": __name__,
                "cls": self.__class__.__name__,
                "args": args
                }, 500

        return {
            "data": {'actor': ActorModel.to_json(actor)},
            "message": "Successfuly adding the actor",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
            }, 201

    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="Missing the ID of the actor")
        args = parser.parse_args()

        if True: #try:
            ActorModel.delete_by_id(args.id)
        else: # except:
            return {
                "data": None,
                "error": "Error during actor deletion, or it don't exists",
                "file": __name__,
                "cls": self.__class__.__name__,
                "args": args
                }, 404

        return {
            "data": None,
            "message": "Successfuly deleting the actor",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
            }, 200


#
# Adding resources:
api.add_resource(Actors, '/v1/actors')
api.add_resource(Actor, '/v1/actor')
