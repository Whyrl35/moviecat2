from passlib.hash import pbkdf2_sha256 as sha256
from flask_sqlalchemy import SQLAlchemy
from run import app

if app.config['DATABASE']['type'] == 'sqlite':
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE']['sqlite']['uri']
elif app.config['DATABASE']['type'] == 'mysql':
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql:///{username}:{password}@{host}/{database}".format(
        username=app.config['DATABASE']['mysql']['user'],
        password=app.config['DATABASE']['mysql']['password'],
        host=app.config['DATABASE']['mysql']['host'],
        database=app.config['DATABASE']['mysql']['database'],
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, phash):
        return sha256.verify(password, phash)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


movie_actors = db.Table('movie_actors',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
)
movie_realisators = db.Table('movie_realisators',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('realisator_id', db.Integer, db.ForeignKey('realisator.id')),
)


class MovieModel(db.Model):
    __tablename__ = 'movie'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    title = db.Column(db.String(255), nullable=False)
    title_original = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    country = db.Column(db.String(255))
    year = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    score = db.Column(db.Integer)
    synopsis = db.Column(db.Text)
    actors = db.relationship('ActorModel', secondary=movie_actors,
                             lazy='subquery',
                             cascade='all',
                             backref=db.backref('movie'))
    realisator = db.relationship('RealisatorModel',
                                 secondary=movie_realisators,
                                 lazy='subquery',
                                 cascade='all',
                                 backref=db.backref('movie'))
    seen = db.Column(db.Boolean, nullable=False)
    trailer = db.Column(db.String(255))
    poster = db.Column(db.String(255))
    background = db.Column(db.String(255))
    is_series = db.Column(db.Boolean, nullable=False)
    series_season = db.Column(db.Integer)
    series_episodes = db.Column(db.Integer)
    series_episode_duration = db.Column(db.Integer)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def to_json(movie):
        return {
            'id': movie.id,
            'title': movie.title,
            'title_original': movie.title_original,
            'genre': movie.genre,
            'country': movie.country,
            'year': movie.year,
            'duration': movie.duration,
            'score': movie.score,
            'synopsis': movie.synopsis,
            'actors': [ ActorModel.to_json(a) for a in movie.actors ],
            'realisators': [ RealisatorModel.to_json(r) for r in movie.realisator ],
            'seen': movie.seen,
            'trailer': movie.trailer,
            'poster': movie.poster,
            'background': movie.background,
            'is_series': movie.is_series,
            'series_season': movie.series_season,
            'series_episodes': movie.series_episodes,
            'series_episode_duration': movie.series_episode_duration
        }

    @classmethod
    def find_by_name(cls, title, year=None, country=None, json=True):
        movie = cls.query.filter_by(title=title, year=year, country=country).first()
        if movie:
            if json:
                return dict(cls.to_json(movie))
            else:
                return movie
        return None

    @classmethod
    def find_by_id(cls, id, json=True):
        movie = cls.query.filter_by(id=id).first()
        if movie:
            if json:
                return dict(cls.to_json(movie))
            else:
                return movie
        return None

    @classmethod
    def return_all(cls):
        return list(map(lambda x: cls.to_json(x), cls.query.all()))

    @classmethod
    def delete_by_id(cls, id):
        movie = cls.query.filter_by(id=id).first()
        if not movie:
            return False
        movie.actors = []
        movie.realisator = []
        db.session.commit()
        cls.query.filter_by(id=id).delete()
        db.session.commit()


class ActorModel(db.Model):
    __tablename__ = 'actor'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def to_json(actor):
        return {
            'id': actor.id,
            'first_name': actor.first_name,
            'last_name': actor.last_name
        }

    @classmethod
    def find_by_name(cls, first_name, last_name, json=True):
        actor = cls.query.filter_by(first_name=first_name, last_name=last_name).first()
        if actor:
            if json:
                return dict(cls.to_json(actor))
            else:
                return actor
        return None

    @classmethod
    def find_by_id(cls, id, json=True):
        actor = cls.query.filter_by(id=id).first()
        if actor:
            if json:
                return dict(cls.to_json(actor))
            else:
                return actor
        return None

    @classmethod
    def return_all(cls):
        return list(map(lambda x: cls.to_json(x), cls.query.all()))

    @classmethod
    def delete_by_id(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()


class RealisatorModel(db.Model):
    __tablename__ = 'realisator'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def to_json(actor):
        return {
            'id': actor.id,
            'first_name': actor.first_name,
            'last_name': actor.last_name
        }

    @classmethod
    def find_by_name(cls, first_name, last_name, json=True):
        realisator = cls.query.filter_by(first_name=first_name, last_name=last_name).first()
        if realisator:
            if json:
                return dict(cls.to_json(realisator))
            else:
                return realisator
        return None

    @classmethod
    def find_by_id(cls, id, json=True):
        realisator = cls.query.filter_by(id=id).first()
        if realisator:
            if json:
                return dict(cls.to_json(realisator))
            else:
                return realisator
        return None

    @classmethod
    def return_all(cls):
        return list(map(lambda x: cls.to_json(x), cls.query.all()))

    @classmethod
    def delete_by_id(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()
