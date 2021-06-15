from flask_restful import Resource
from models.virus_total_model import VirusTotalModel
class VirusTotalAPI(Resource):

    @staticmethod
    def get(domain):
        return VirusTotalModel.find_by_domain(domain).json()

    @staticmethod
    def put(domain):
        pass