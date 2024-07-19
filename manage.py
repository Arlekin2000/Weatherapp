import argparse

from app.main import app
from app.models import User, City, UserHistory, db


def args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-init_db', required=False, action='store_true')
    parser.add_argument('-run', required=False, action='store_true')
    return parser


if __name__ == "__main__":
    parser = args_parser()
    namespace = parser.parse_args()

    if namespace.init_db:
        db.create_tables([User, City, UserHistory])

    if namespace.run:
        app.run(debug=True)
