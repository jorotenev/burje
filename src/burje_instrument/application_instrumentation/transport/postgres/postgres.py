from datetime import datetime
from typing import List, Iterator

from sqlalchemy.orm import Session

from burje_instrument.application_instrumentation.transport.postgres.models import MeasurementRecord
from burje_instrument.application_instrumentation.transport.transport import Transport
from burje_instrument.dto import Measurement
from burje_instrument.application_instrumentation.transport.postgres.raw import session


class PostgresTransport(Transport):
    def __init__(self):
        self._s: Session = session

    def persist_measurements(self, measurements: List[Measurement]):
        records: Iterator[MeasurementRecord] = map(MeasurementRecord.from_measurement, measurements)
        self._s.bulk_save_objects(records)
        self._s.commit()


if __name__ == '__main__':
    # engine = make_engine()
    # create_table(engine)

    re = MeasurementRecord.from_measurement(
        Measurement(metric='asd', unit='seconds', value=1.0, created_at=datetime.utcnow(), dimensions={'a': 1}))
    print(re)
    t = PostgresTransport(session=session)
    print(t)
    records = t._s.query(MeasurementRecord).all()
    for r in records:
        print(r)
