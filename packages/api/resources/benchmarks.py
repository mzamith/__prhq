from api.dao.benchmark_dao import BenchmarkDAO
from flask_restful import Resource
from flask_jwt_extended import jwt_required
import json

dao = BenchmarkDAO()

class AllGirlsResouce(Resource):
    @jwt_required
    def get(self):
        return json.dumps([girl.__dict__ for girl in dao.return_all_girls()])
        