from flask_restful import Resource
from notes.db import get_db


class Directory(Resource):
    def get(self):
        db = get_db()
        result = db.execute(
            'SELECT filename FROM note'
        ).fetchall()

        filenames = [entry[0] for entry in result]

        return {'filenames': filenames}
