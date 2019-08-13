from api.app import db
import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

class Auditable(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.String(64))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_by = db.Column(db.String(64))

class Affiliate(Auditable):
    __tablename__ = 'affiliate'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.Text, index=False, unique=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

class User(Auditable):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    affiliate_id = db.Column(db.Integer, db.ForeignKey(Affiliate.id))
    affiliate = relationship('Affiliate')
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<id {}>'.format(self.id)


class WorkoutTypes(db.Model):
    __tablename__ = 'workout_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(64), index=False, unique=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ScoreTypes(db.Model):
    __tablename__ = 'score_types'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Movement(db.Model):
    __tablename__ = 'movement'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), index=True, unique=True)
    standard = db.Column(db.String(64))

    def __repr__(self):
        return '<id {}>'.format(self.id)

lift_association_table = db.Table('lift_association', db.Model.metadata,
    db.Column('lift_id', db.Integer, db.ForeignKey('lift.id')),
    db.Column('movement_id', db.Integer, db.ForeignKey('movement.id'))
)

benchmark_association_table = db.Table('benchmark_association', db.Model.metadata,
    db.Column('benchmark_id', db.Integer, db.ForeignKey('benchmark.id')),
    db.Column('movement_id', db.Integer, db.ForeignKey('movement.id'))
)

custom_wod_association_table = db.Table('custom_workout_association', db.Model.metadata,
    db.Column('custom_workout_id', db.Integer, db.ForeignKey('custom_workout.id')),
    db.Column('movement_id', db.Integer, db.ForeignKey('movement.id'))
)

class Lift(db.Model):

    __tablename__ = 'lift'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    workout_type_id = db.Column(db.Integer, db.ForeignKey('workout_types.id'))
    workout_type = relationship('WorkoutTypes')
    score_type_id = db.Column(db.Integer, db.ForeignKey('score_types.id'))
    score_type = relationship('ScoreTypes')
    movements = relationship('Movement', secondary=lift_association_table)
    lift_records = relationship('LiftRecord', back_populates='lift')

class Benchmark(db.Model):

    __tablename__ = 'benchmark'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    workout_type_id = db.Column(db.Integer, db.ForeignKey('workout_types.id'))
    workout_type = relationship('WorkoutTypes')
    score_type_id = db.Column(db.Integer, db.ForeignKey('score_types.id'))
    score_type = relationship('ScoreTypes')
    movements = relationship('Movement', secondary=benchmark_association_table)

class CustomWorkout(db.Model):

    __tablename__ = 'custom_workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    workout_type_id = db.Column(db.Integer, db.ForeignKey('workout_types.id'))
    workout_type = relationship('WorkoutTypes')
    score_type_id = db.Column(db.Integer, db.ForeignKey('score_types.id'))
    score_type = relationship('ScoreTypes')
    movements = relationship('Movement', secondary=custom_wod_association_table)

class LiftRecord(Auditable):

    __tablename__ = 'lift_record'
    id = db.Column(db.Integer, primary_key=True)
    lift_id = db.Column(db.Integer, db.ForeignKey('lift.id'))
    lift = relationship('Lift', back_populates='lift_records')
    number_of_sets = db.Column(db.Integer)
    reps_per_set = db.Column(db.Integer)
    date = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    sets = relationship('SetRecord')

class SetRecord(Auditable):

    __tablename__ = 'set_record'
    id = db.Column(db.Integer, primary_key=True)
    rep_number = db.Column(db.Integer)
    score = db.Column(db.Integer)
    lift_record_id = db.Column(db.Integer, db.ForeignKey('lift_record.id'))


