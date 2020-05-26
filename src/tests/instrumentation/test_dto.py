import json
from datetime import datetime
from unittest import TestCase

from burje_instrument.dto import Unit, Measurement


class TestMeasuremet(TestCase):

    def test_to_json(self):
        now = datetime.utcnow()
        metric = 'some_metric'
        dimensions = {'d1': 'v1'}
        some_val = 1
        unit = Unit.seconds
        measurement = Measurement(created_at=now, metric=metric, dimensions=dimensions, value=some_val,
                                  unit=unit)

        loaded_dict = json.loads(measurement.to_json())
        self.assertDictEqual({
            'created_at': now.isoformat(),
            'metric': metric,
            'dimensions': dimensions,
            'value': some_val,
            'unit': unit.name
        }, loaded_dict)
