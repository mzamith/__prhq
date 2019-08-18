from api.app import db
import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
import enum
import json

class Auditable(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.String(64))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_by = db.Column(db.String(64))

class Affiliate(Auditable):
    __tablename__ = 'affiliate'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64))
    address = db.Column(db.Text, index=False, unique=False)

    def __init__(self, code, name, address = None):
        self.name = name
        self.code = code
        self.address = address

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

    def __init__(self, username, email, password, affiliate):
        self.username = username
        self.email = email
        self.password_hash = password
        self.affiliate = affiliate
        self.affiliate_id = affiliate.id


    def __repr__(self):
        return '<username {}>'.format(self.username)


class WorkoutTypeEnum(enum.Enum):
    notable = 'NTB'
    games = 'GMS'
    gymnastics = 'GYM'
    endurance = 'END'
    lift = 'LFT'
    barbell_complex = 'CPX'
    custom = 'CTM'
    girls = 'GRL'
    heroes = 'HRS'
    other = 'OTH'

class WorkoutCategoryEnum(enum.Enum):
    benchmark = 'BCH'
    barbell = 'BBL'
    other = 'OTH'

class WorkoutTypes(db.Model):
    __tablename__ = 'workout_types'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Enum(WorkoutTypeEnum))
    label = db.Column(db.String(64), index=True, unique=True)
    category = db.Column(db.Enum(WorkoutCategoryEnum))
    description = db.Column(db.String(64), index=False, unique=False)

    def __init__(self, code, label, category, description = None):
        self.code = code
        self.label = label
        self.category = category
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ScoreTypes(db.Model):
    __tablename__ = 'score_types'

    def __init__(self, code, label):
        self.code = code
        self.label = label

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), index=True, unique=True)
    label = db.Column(db.String(64))

    def __repr__(self):
        return '<id {}>'.format(self.id)

class MeasurementEnum(enum.Enum):
    distance = 'DISTANCE'
    weight = 'WEIGHT'
    height = 'HEIGHT'


class Movement(db.Model):
    __tablename__ = 'movement'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5))
    label = db.Column(db.String(64), index=True, unique=True)
    standard = db.Column(db.String(64))
    load_measurement = db.Column(db.Enum(MeasurementEnum))

    def __init__(self, code, label, load=None):
        self.code = code
        self.label = label
        self.load_measurement = load

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
    
    def __init__(self, name, workout_type, score_type):
        self.name = name
        self.workout_type = workout_type
        self.workout_type_id = workout_type.id
        self.score_type = score_type
        self.score_type_id = score_type.id

    def get_pr(self):
        return max(lift_records, key=lambda x: x.get_highest())



class Benchmark(db.Model):

    __tablename__ = 'benchmark'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    workout_type_id = db.Column(db.Integer, db.ForeignKey('workout_types.id'))
    workout_type = relationship('WorkoutTypes')
    score_type_id = db.Column(db.Integer, db.ForeignKey('score_types.id'))
    score_type = relationship('ScoreTypes')
    movements = relationship('Movement', secondary=benchmark_association_table)

    def __init__(self, name, workout_type, score_type):
        self.name = name
        self.workout_type = workout_type
        self.workout_type_id = workout_type.id
        self.score_type = score_type
        self.score_type_id = score_type.id

label_wod_association_table = db.Table('label_association', db.Model.metadata,
    db.Column('custom_workout_id', db.Integer, db.ForeignKey('custom_workout.id')),
    db.Column('label_id', db.Integer, db.ForeignKey('label.id'))
)


class CustomWorkout(db.Model):

    __tablename__ = 'custom_workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    workout_type_id = db.Column(db.Integer, db.ForeignKey('workout_types.id'))
    workout_type = relationship('WorkoutTypes')
    score_type_id = db.Column(db.Integer, db.ForeignKey('score_types.id'))
    score_type = relationship('ScoreTypes')
    labels = relationship('Label', secondary=label_wod_association_table)
    movements = relationship('Movement', secondary=custom_wod_association_table)

    def __init__(self, name, workout_type, score_type):
        self.name = name
        self.workout_type = workout_type
        self.workout_type_id = workout_type.id
        self.score_type = score_type
        self.score_type_id = score_type.id

class LiftRecord(Auditable):

    __tablename__ = 'lift_record'
    id = db.Column(db.Integer, primary_key=True)
    lift_id = db.Column(db.Integer, db.ForeignKey('lift.id'))
    lift = relationship('Lift', back_populates='lift_records')
    number_of_sets = db.Column(db.Integer)
    reps_per_set = db.Column(db.Integer)
    date = db.Column(db.DateTime, default = datetime.datetime.utcnow)
    sets = relationship('SetRecord')

    def __init__(self, number_of_sets, reps_per_set):
        self.number_of_sets = number_of_sets
        self.reps_per_set = reps_per_set

    def get_highest(self):
        return max(sets, key=lambda x: x.score)


class SetRecord(Auditable):

    __tablename__ = 'set_record'
    id = db.Column(db.Integer, primary_key=True)
    set_number = db.Column(db.Integer)
    score = db.Column(db.Integer)
    lift_record_id = db.Column(db.Integer, db.ForeignKey('lift_record.id'))

    def __init__(self, set_number, score):
        self.set_number = set_number
        self.score = score

class Label(Auditable):

    __tablename__ = 'label'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
