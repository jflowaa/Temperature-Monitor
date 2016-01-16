from flask import render_template, url_for
from .. import db
from ..models import Record
from . import main
from flask import request
from datetime import datetime
import pygal
from pygal.style import DefaultStyle


@main.route('/')
def index():
    title = "Temperature Monitor"
    chart = pygal.StackedLine(title=title, width=1200, x_title="Time (CST)",
            y_title="Temperature (F)", fill=True, interpolate='cubic',
            style=DefaultStyle)
    records = Record.query.all()
    times = []
    temps = []
    for record in records:
        time = str(record.time).split(":")
        time[0] = int(time[0]) - 6
        times.append("{}:{}".format(str(time[0]), time[1]))
        temps.append(record.temperature)
    chart.x_labels = times[-20:]
    chart.add("Room Name", temps[-20:])
    return render_template("index.html", title=title, chart=chart)


@main.route('/addrecord', methods=['POST'])
def add_record():
    temp = request.form["temperature"]
    time = datetime.time(datetime.utcnow())
    record = Record(temperature=temp, time=time)
    db.session.add(record)
    return "200"
