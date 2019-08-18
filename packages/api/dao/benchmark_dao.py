from api.models import Benchmark, WorkoutTypes, WorkoutTypeEnum
from api.app import db

class BenchmarkDAO:

    def return_all_girls(self):
        return db.session.query(Benchmark).join(WorkoutTypes).filter(WorkoutTypes.code == WorkoutTypeEnum.girls).all()
