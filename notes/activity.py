from flask_restful import Resource, reqparse
from notes.db import get_db
from matplotlib import pyplot as plt
from io import BytesIO
from base64 import b64encode
import time

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument("changed_words", required=True, type=int)


class Activity(Resource):
    def get(self):
        db = get_db()
        records = db.execute(
            'SELECT words, int_time'
            '  FROM activity'
            '  ORDER BY'
            '    int_time DESC'
        ).fetchall()

        words_activity = [record[0] for record in records]

        # Standardise times
        times = [record[1] for record in records]
        min_time = min(times)
        time_activity = [record[1] - min_time for record in records]

        plt.figure(1)
        plt.plot(time_activity, words_activity, 'ro', ls='-')
        axes = plt.gca()
        axes.set_xlabel('Time (Sec)')
        axes.set_ylabel('Activity (Words)')
        axes.set_xlim([0, max(time_activity) + 1])
        axes.set_ylim([0, max(words_activity) + 1])

        temp_file = BytesIO()

        plt.savefig(temp_file, format='png')
        b64_data = b64encode(temp_file.getvalue())\
            .decode('utf-8')\
            .replace('\n', '')

        return {'data': b64_data}

    def post(self):
        args = parser.parse_args()
        changed_words = args['changed_words']

        db = get_db()
        db.execute(
            'INSERT INTO activity (words, int_time)'
            '  VALUES (?, ?)',
            (changed_words, int(time.time()))
        )

        db.commit()
