from sqlalchemy import Column, Integer, DateTime, String, Float, JSON

from burje_instrument.application_instrumentation.transport.postgres.raw import Base
from burje_instrument.dto import Measurement



class MeasurementRecord(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    metric = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    dimensions = Column(JSON)
    unit = Column(String)

    def __repr__(self):
        return f'MeasurementRecord(metric={self.metric}, value={self.value}, created_at={self.created_at}, dimensions={self.dimensions}, unit={self.unit})'

    @classmethod
    def from_measurement(cls, measurement: Measurement) -> 'MeasurementRecord':
        return MeasurementRecord(created_at=measurement.created_at,
                                 metric=measurement.metric, value=measurement.value,
                                 unit=measurement.unit, dimensions=measurement.dimensions)
