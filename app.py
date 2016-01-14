import os
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request
from datetime import datetime
import pygal

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['secretkey'] or "qewrndf%*234+k"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = False 

db = SQLAlchemy(app)
boostrap = Bootstrap(app)


class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return "Record: Temperature {}, Time {}".format(self.temperature, self.time)


@app.route('/')
def index():
    title = "Temperature Monitor"
    chart = pygal.Line(width=1200, height=600, explicit_size=False, title=title, x_title="Time", y_title="Temperature in C")
    records = Record.query.all()
    times = []
    temps = []
    for record in records:
        time = str(record.time).split(":")
        times.append(time[0] + ":" + time[1])
        temps.append(record.temperature)
    chart.x_labels = times[-10:]
    chart.add("Living Room", temps[-10:])
    return render_template('index.html', title=title, chart=chart)


@app.route('/addrecord', methods=['POST'])
def add_record():
    temp = request.form["temperature"]
    time = datetime.time(datetime.now())
    record = Record(temperature=temp, time=time)
    db.session.add(record)
    return "200"

if __name__ == '__main__':
    app.run()
