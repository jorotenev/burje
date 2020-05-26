from flask import render_template

from burje_instrument.application_instrumentation.transport.postgres.models import MeasurementRecord
from . import main
from logging import info
from burje_instrument.application_instrumentation.transport.postgres.raw import session

from burje_instrument.application_instrumentation.decorator import *
from threading import current_thread


@main.route('/', methods=['GET', 'POST'])
def index():
    info('opsa')
    print(f"FLASK RUNNING IN {current_thread()}")
    records = session.query(MeasurementRecord).all()
    return render_template('index.html', extra={i: msr for i, msr in enumerate(list(records))})
