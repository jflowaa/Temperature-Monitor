from flask import render_template, url_for
from .. import db
from ..models import Record
from . import main
from flask import request
from datetime import datetime
from dateutil import tz
import pygal
from pygal.style import DefaultStyle


@main.route('/')
def index():
    title = "Temperature Monitor"
    chart = pygal.StackedLine(title=title, width=1200, x_title="Time (CST)",
            y_title="Temperature (F)", fill=True, interpolate='hermite',
            style=DefaultStyle, print_values=True,
            disable_xml_declaration=True)
    records = reversed(Record.query.order_by(Record.id.desc()).limit(18).all())
    times = []
    temps = []
    for record in records:
        time = record.time.strftime("%I:%M %p")
        times.append(str(time))
        temps.append(record.temperature)
    chart.x_labels = times
    chart.add("Room Name", temps)
    chart.value_formatter = lambda x: "%.2f" % x
    return render_template("index.html", title=title, chart=chart)


@main.route('/addrecord', methods=['POST'])
def add_record():
    temp = request.form["temperature"]
    time = datetime.time(datetime.now(tz.gettz('US/Central')))
    record = Record(temperature=temp, time=time)
    db.session.add(record)
    return "200"
