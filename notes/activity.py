from flask_restful import Resource, reqparse
from notes.db import get_db

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument("changed_words", required=True, type=int)

class Activity(Resource):
    def get(self):
        # cool stuff
        pass

    def post(self):
        args = parser.parse_args()

