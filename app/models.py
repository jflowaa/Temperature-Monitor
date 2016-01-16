from . import db


class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    time = db.Column(db.Time, nullable=False)


    def __repr(self):
        return "Record: Temperature {}, Time {}".format(self.temperature, self.time)
