from flask_restful import Resource, reqparse
from notes.db import get_db

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument("filename", type=str, help="File doesn't exist")
parser.add_argument('content', type=str, location='json')


class File(Resource):
    def get(self, filename):
        db = get_db()
        content = db.execute(
            'SELECT content'
            '  FROM note'
            '  WHERE filename = ?',
            (filename,)
        ).fetchone()[0]

        return content

    def post(self, filename):
        args = parser.parse_args()
        content = args["content"]

        db = get_db()

        exists = db.execute(
            'SELECT 1 FROM note WHERE filename = ?', (filename,)
        ).fetchone()

        if exists:
            print('updating')
            db.execute(
                'UPDATE note SET content = ?'
                '  WHERE filename = ?',
                (content, filename)
            )
        else:
            print('inserting')
            db.execute(
                'INSERT INTO note (content, filename)'
                '  VALUES (?, ?)',
                (content, filename)
            )

        db.commit()
