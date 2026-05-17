import sqlalchemy
import sqlalchemy.orm as orm

SqlAlchemyBase = orm.declarative_base()


class UserProfile(SqlAlchemyBase):
    __tablename__ = 'users'

    user_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    height = sqlalchemy.Column(sqlalchemy.Integer)
    weight = sqlalchemy.Column(sqlalchemy.Float)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    gender = sqlalchemy.Column(sqlalchemy.String)
    level = sqlalchemy.Column(sqlalchemy.String)
    goal = sqlalchemy.Column(sqlalchemy.String)
    targ_kg = sqlalchemy.Column(sqlalchemy.Float)
    activ = sqlalchemy.Column(sqlalchemy.String, default="moderate")
    bmi = sqlalchemy.Column(sqlalchemy.Float)
    tde = sqlalchemy.Column(sqlalchemy.Integer)
    last_wrkt = sqlalchemy.Column(sqlalchemy.String)
    streak = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    work_done = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    step = sqlalchemy.Column(sqlalchemy.String)

    history = sqlalchemy.Column(sqlalchemy.JSON, default=list)