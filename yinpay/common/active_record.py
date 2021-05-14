from flask_restplus import abort
from sqlalchemy import exc
from sqlalchemy_utils import Timestamp

from yinpay.ext import db


class Record(Timestamp):
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            abort(500, e.__str__())

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            abort(500, e.__str__())
            db.session.rollback()
