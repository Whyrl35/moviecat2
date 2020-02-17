from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from run import app, api
from .models import MovieModel, ActorModel, RealisatorModel
from sqlalchemy import func
import re


class GlobalStatistics(Resource):
    def get(self):
        stats = {}

        count_q = MovieModel.query.filter(MovieModel.is_series == False).statement.with_only_columns([func.count()])
        sum_duration_q = MovieModel.query.filter(MovieModel.is_series == False).statement.with_only_columns([func.sum(MovieModel.duration)])
        avg_duration_q = MovieModel.query.filter(MovieModel.is_series == False).statement.with_only_columns([func.avg(MovieModel.duration)])
        avg_score_q = MovieModel.query.filter(MovieModel.is_series == False).statement.with_only_columns([func.avg(MovieModel.score)])
        stats['movies'] = {
            'count': int(MovieModel.query.session.execute(count_q).scalar()),
            'duration': {
                'total': int(MovieModel.query.session.execute(sum_duration_q).scalar()),
                'avg': float(MovieModel.query.session.execute(avg_duration_q).scalar()),
            },
            'score': float(MovieModel.query.session.execute(avg_score_q).scalar()),
        }

        count_q = MovieModel.query.filter(MovieModel.is_series == True).statement.with_only_columns([func.count()])
        sum_q = MovieModel.query.filter(MovieModel.is_series == True).statement.with_only_columns([func.sum(MovieModel.series_episodes)])
        sum_duration_q = MovieModel.query.filter(MovieModel.is_series == True).statement.with_only_columns([func.sum(MovieModel.duration)])
        avg_duration_q = MovieModel.query.filter(MovieModel.is_series == True).statement.with_only_columns([func.avg(MovieModel.duration)])
        avg_score_q = MovieModel.query.filter(MovieModel.is_series == True).statement.with_only_columns([func.avg(MovieModel.score)])
        stats['series'] = {
            'count': int(MovieModel.query.session.execute(count_q).scalar()),
            'episodes': int(MovieModel.query.session.execute(sum_q).scalar()),
            'duration': {
                'total':  int(MovieModel.query.session.execute(sum_duration_q).scalar()),
                'avg': float(MovieModel.query.session.execute(avg_duration_q).scalar()),
            },
            'score': float(MovieModel.query.session.execute(avg_score_q).scalar()),
        }

        movies = MovieModel.return_all(json=False)
        all_genres = {}
        for movie in movies:
            genres = re.split(',|/|;| |&', movie.genre)
            for genre in genres:
                low = genre.lower().strip()
                if low != '':
                    if low not in all_genres:
                        all_genres[low] = 0
                    all_genres[low] += 1

        stats['genres'] = {
            'count':  int(len(all_genres.keys())),
            'count_by_genres': all_genres
        }

        count_seen_q = MovieModel.query.filter(MovieModel.seen == True).statement.with_only_columns([func.count()])
        count_total_q = MovieModel.query.statement.with_only_columns([func.count()])
        stats['seen'] = {
            'total': int(MovieModel.query.session.execute(count_total_q).scalar()),
            'seen': int(MovieModel.query.session.execute(count_seen_q).scalar()),
        }

        return {
            "data": stats,
            "message": "Successfuly returning the global's statistics",
            "file": __name__,
            "cls": self.__class__.__name__,
            "args": None
        }, 200


#
# Adding resources:
api.add_resource(GlobalStatistics, '/v1/statistics')
