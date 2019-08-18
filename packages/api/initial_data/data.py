from api.models import *
from api.utils import import_json
import sys

def create_score_types():

    st_list = [
        ScoreTypes('TIME', 'Time'),
        ScoreTypes('REPS', 'Reps'),
        ScoreTypes('ROUNDS_AND_REPS', 'Ronds and Reps'),
        ScoreTypes('LOAD', 'Load'),
        ScoreTypes('QUALITY', 'Quality'),
        ScoreTypes('TEXT', 'Text'),
        ScoreTypes('POINTS', 'Points'),
        ScoreTypes('CALORIES', 'Calories'),
        ScoreTypes('DISTANCE', 'Distance')
    ]

    return st_list

def create_workout_types():

    wt_list = [
        WorkoutTypes(WorkoutTypeEnum.notable, 'Notables', WorkoutCategoryEnum.benchmark),
        WorkoutTypes(WorkoutTypeEnum.games, 'Games', WorkoutCategoryEnum.benchmark),
        WorkoutTypes(WorkoutTypeEnum.gymnastics, 'Gymastics', WorkoutCategoryEnum.benchmark),
        WorkoutTypes(WorkoutTypeEnum.endurance, 'Endurance', WorkoutCategoryEnum.benchmark),
        WorkoutTypes(WorkoutTypeEnum.lift, 'Lifts', WorkoutCategoryEnum.barbell),
        WorkoutTypes(WorkoutTypeEnum.barbell_complex, 'Barbell Complexes', WorkoutCategoryEnum.barbell),
        WorkoutTypes(WorkoutTypeEnum.custom, 'Custom', WorkoutCategoryEnum.benchmark),
        WorkoutTypes(WorkoutTypeEnum.girls, 'Girls', WorkoutCategoryEnum.benchmark),
        WorkoutTypes(WorkoutTypeEnum.heroes, 'Heroes', WorkoutCategoryEnum.benchmark),
        WorkoutTypes(WorkoutTypeEnum.other, 'Other', WorkoutCategoryEnum.benchmark)
    ]

    return wt_list


def create_benchmarks(workout_types_dict, score_types_dict, movements_dict):

    b = Benchmark("Run 5k", workout_types_dict[WorkoutTypeEnum.endurance], score_types_dict['TIME'])
    b.movements.append(movements_dict['RUN'])

    fran = Benchmark("Fran", workout_types_dict[WorkoutTypeEnum.girls], score_types_dict['TIME'])
    fran.movements.append(movements_dict['THR'])
    fran.movements.append(movements_dict['PU'])
    grace = Benchmark("Grace", workout_types_dict[WorkoutTypeEnum.girls], score_types_dict['TIME'])
    grace.movements.append(movements_dict['CAJ'])

    b_list = [
        b,
        fran,
        grace
    ]

    return b_list

def create_lift(workout_types_dict, score_types_dict, movements_dict):

    sr1= SetRecord(1, 50)
    sr2= SetRecord(2, 60)

    lr = LiftRecord(2, 1)
    lr.sets.append(sr1)
    lr.sets.append(sr2)

    l = Lift("Power Snatch", workout_types_dict[WorkoutTypeEnum.lift], score_types_dict['LOAD'])
    l.movements.append(movements_dict['PS'])
    l.lift_records.append(lr)

    l_list = [
        l
    ]

    return l_list

def create_movements():

    m_list = [
        Movement("HSPU", 'Handstand Push-Up'),
        Movement("PS", 'Power Snatch', MeasurementEnum.weight),
        Movement("RUN", 'Running', MeasurementEnum.distance),
        Movement("THR", 'Thruster', MeasurementEnum.weight),
        Movement("PU", 'Pull-Up'),
        Movement("CAJ", 'Clean and Jerk', MeasurementEnum.weight)
    ]

    return m_list

def load_initial_data(db):

    # 1.
    # Affiliate
    affiliate = Affiliate('N14', 'N14 Crossfit', 'Braga')
    db.session.add(affiliate)

    # 2.
    # Score Types - Time, Reps
    db.session.bulk_save_objects(create_score_types())

    # 3.
    # Workout Types
    db.session.bulk_save_objects(create_workout_types())

    # 4.
    # Movements
    db.session.bulk_save_objects(create_movements())
    db.session.commit()

    user = User('MZ', '', 
    '$pbkdf2-sha256$29000$XesdA6B0rhUiROhdS0mpVQ$yr8j52fw4QN8dA0oUQn7WSJ.3mMXbVhmSDSwJNDuqjU',
    db.session.query(Affiliate).filter(Affiliate.code == 'N14').one())
    db.session.add(user)

    score_types = db.session.query(ScoreTypes)
    score_types_dict = {s.code : s for s in score_types}

    workout_types = db.session.query(WorkoutTypes)
    workout_types_dict = {s.code : s for s in workout_types}

    movements = db.session.query(Movement)
    movements_dict = {s.code : s for s in movements}

    # 5.
    # Benchmarks
    db.session.add_all(create_benchmarks(workout_types_dict, score_types_dict, movements_dict))
    db.session.add_all(create_lift(workout_types_dict, score_types_dict, movements_dict))
    db.session.commit()



