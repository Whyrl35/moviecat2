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


movie_actors = db.Table('actors',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
)
movie_realisators = db.Table('realisators',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('realisator_id', db.Integer, db.ForeignKey('realisator.id'), primary_key=True),
)


class Movie(db.Model):
    __tablename__ = 'movies'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    title_original = db.Column(db.String(255))
    genre = db.Column(db.String(255))
    country = db.Column(db.String(255))
    year = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    score = db.Column(db.Integer)
    synopsis = db.Column(db.Text)
    synopsis = db.Column(db.Text)
    actors = db.relationship('Actor', secondary=movie_actors,
                             lazy='subquery',
                             backref=db.backref('movies', primary_key=True))
    realisator = db.relationship('Realisator',
                                 secondary=movie_realisators,
                                 lazy='subquery',
                                 backref=db.backref('movies', primary_key=True))
    synopsis = db.Column(db.Text)
    seen = db.Column(db.Boolean, nullable=False)
    trailer = db.Column(db.String(255))
    poster = db.Column(db.String(255))
    background = db.Column(db.String(255))
    is_series = db.Column(db.Boolean, nullable=False)
    series_season = db.Column(db.Integer)
    series_episodes = db.Column(db.Integer)
    series_episode_duration = db.Column(db.Integer)


class Actor(db.Model):
    __tablename__ = 'actors'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)


class Realisator(db.Model):
    __tablename__ = 'realisators'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
