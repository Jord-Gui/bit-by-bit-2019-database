from flask_restful import Resource, reqparse
from notes.db import get_db
from matplotlib import pyplot as plt
from io import BytesIO
from base64 import b64encode
import time
import numpy as np
from scipy.interpolate import interp1d


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

        if not records:
            return {'data': ''}

        # Words
        words_activity = [record[0] for record in records]
        words_activity.reverse()

        # Standardise times
        times = [record[1] for record in records]
        min_time = min(times)
        time_activity = [value - min_time for value in times]
        time_activity.reverse()

        spl = interp1d(time_activity, words_activity, kind='cubic')
        xnew = np.linspace(min(time_activity), max(time_activity), 200)
        words_smooth = spl(xnew)

        fig = plt.figure(1)
        fig.patch.set_facecolor("#eeeeee")
        line, = plt.plot(xnew, words_smooth, ls='-')
        line.set_color("#00adb5")
        axes = plt.gca()
        axes.set_xlabel('Time (Sec)', color="#303841")
        axes.set_ylabel('Activity (Words)', color="#303841")
        axes.patch.set_facecolor("#eeeeee")
        axes.set_xlim([0, max(time_activity)])
        axes.set_ylim([0, max(words_activity)])

        temp_file = BytesIO()

        plt.savefig(temp_file, format='png', facecolor=fig.get_facecolor())
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
