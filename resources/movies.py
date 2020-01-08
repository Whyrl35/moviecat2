from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from run import app, api
from .models import MovieModel, ActorModel, RealisatorModel


class Movies(Resource):
    # @swag_from('./../docs/movies_list.yml')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, action='append', required=False, help="List of movie's id")
        args = parser.parse_args()

        if args.id:
            movies_list = list()
            for id in args.id:
                movies_list.append(MovieModel.find_by_id(id))
            movies = {'movies': movies_list}
        else:
            movies = {'movies': MovieModel.return_all()}

        return {
            "data": movies,
            "message": "Successfuly returning the movie list",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
        }, 200

    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, action='append', required=True, help="Missing list of movie's id")
        args = parser.parse_args()

        movies_list = list()
        for id in args.id:
            movie = MovieModel.find_by_id(id)
            if movie:
                MovieModel.delete_by_id(id)
                movies_list.append(movie)

        movies = {'movies': movies_list}
        return {
            "data": movies,
            "message": "Successfuly deleting the realisator list",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
        }, 201

class Movie(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="Missing the id of the movie")
        args = parser.parse_args()

        try:
            movie = MovieModel.find_by_id(args.id)
        except AttributeError:
            return {
                "data": None,
                "error": "movie with this id doesn't exist",
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
            "data": { 'movie': movie },
            "message": "Successfuly fetching movie",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
            }, 200

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help="Missing the title")
        parser.add_argument('title_original', type=str, required=True, help="Missing the original title")
        parser.add_argument('genre', type=str, required=True, help="Missing the genre")
        parser.add_argument('country', type=str, required=True, help="Missing the country")
        parser.add_argument('year', type=int, required=True, help="Missing the year of production")
        parser.add_argument('duration', type=int, required=True, help="Missing the duration in minutes of the film")
        parser.add_argument('score', type=float, required=False, help="Missing your score for the film")
        parser.add_argument('synopsis', type=str, required=True, help="Missing the synopsis of the film")
        parser.add_argument('actors', type=str, required=True, help="Missing the actors")
        parser.add_argument('realisators', type=str, required=True, help="Missing the realisators")
        parser.add_argument('seen', type=bool, required=False, help="Missing the seen flag")
        parser.add_argument('trailer', type=str, required=False, help="Missing the trailer url")
        parser.add_argument('poster', type=str, required=False, help="Missing the trailer url")
        parser.add_argument('background', type=str, required=False, help="Missing the trailer url")
        parser.add_argument('is_series', type=bool, required=False, help="Missing the series flag")
        parser.add_argument('series_season', type=int, required=False, help="Missing the serie's season")
        parser.add_argument('series_episodes', type=int, required=False, help="Missing the serie's episodes numbers")
        parser.add_argument('series_episodes_duration', type=int, required=False, help="Missing the serie's episodes duration in minutes")
        args = parser.parse_args()

        movie = MovieModel.find_by_name(args.title, year=args.year, country=args.country)
        if movie:
            return {
                "data": {'movie': movie},
                "message": "Movie already exists",
                "file": __name__,
                "cls": self.__class__.__name__,
                "args": args
                }, 200
        try:
            movie = MovieModel()
            movie.title = args.title
            movie.title_original = args.title_original
            movie.title = args.title
            movie.title_original = args.title_original
            movie.genre = args.genre
            movie.country = args.country
            movie.year = args.year
            movie.duration = args.duration
            movie.score = args.score
            movie.synopsis = args.synopsis
            movie.seen = args.seen
            movie.trailer = args.trailer
            movie.poster = args.poster
            movie.background = args.background
            movie.is_series = args.is_series
            movie.series_season = args.series_season
            movie.series_episodes = args.series_episodes
            movie.series_episodes_duration = args.series_episodes_duration

            for actor_str in args.actors.split(','):
                first, *last = actor_str.split()
                last = " ".join(last)
                actor = ActorModel.find_by_name(first, last, json=False)
                if actor:
                    movie.actors.append(actor)
                else:
                    actor = ActorModel()
                    actor.first_name = first
                    actor.last_name = last
                    actor.save_to_db()
                    movie.actors.append(actor)

            for realisator_str in args.realisators.split(','):
                first, *last = realisator_str.split()
                last = " ".join(last)
                realisator = RealisatorModel.find_by_name(first, last, json=False)
                if realisator:
                    movie.realisator.append(realisator)
                else:
                    realisator = RealisatorModel()
                    realisator.first_name = first
                    realisator.last_name = last
                    realisator.save_to_db()
                    movie.realisator.append(realisator)

            movie.save_to_db()

        except:
            return {
                "data": None,
                "error": "Error during movie creation",
                "file": __name__,
                "cls": self.__class__.__name__,
                "args": args
                }, 500
        return {
            "data": {'movie': MovieModel.to_json(movie)},
            "message": "Successfuly adding the realisator",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
            }, 201

    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, help="Missing the ID of the movie")
        args = parser.parse_args()

        #try:
        if True:
            MovieModel.delete_by_id(args.id)
        #except:
        else:
            return {
                "data": None,
                "error": "Error during movie deletion, or it don't exists",
                "file": __name__,
                "cls": self.__class__.__name__,
                "args": args
                }, 404

        return {
            "data": None,
            "message": "Successfuly deleting the movie",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": args
            }, 200
#
# Adding resources:
api.add_resource(Movies, '/v1/movies')
api.add_resource(Movie, '/v1/movie')
