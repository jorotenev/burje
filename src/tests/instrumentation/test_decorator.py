import asyncio
import json
from datetime import datetime
from time import sleep
from unittest import TestCase
from unittest.mock import patch

from burje_instrument.application_instrumentation.decorator import Instrumentor
from burje_instrument.dto import Unit, Measurement
from tests.utilities import ObsoleteAsyncTestCase

TOLERANCE = 0.05

test_metric = 'test_metric'
test_unit = Unit.seconds
_ins_test = Instrumentor(metric=test_metric, unit=test_unit)


@_ins_test
async def target_decorated_function(sleep_for=.5):
    from asyncio import sleep
    await sleep(sleep_for)
    return 1


@patch('burje_instrument.application_instrumentation.decorator.buffer')
class TestSmoke(ObsoleteAsyncTestCase):
    def test_decorated_returns_value(self, _):
        result = self._run(target_decorated_function(sleep_for=0.1))
        self.assertEqual(result, 1)

    def test_decorated_can_raise_exception(self, _):
        class CustomException(Exception): ...

        @_ins_test
        async def target_raising_function():
            raise CustomException('some exception')

        with self.assertRaisesRegex(CustomException, 'some exception'):
            self._run(target_raising_function())

    def test_sends_to_buffer(self, mocked_buffer):
        self._run(target_decorated_function())
        mocked_buffer.put_nowait.assert_called_once()

    def test_correct_measurement(self, mocked_buffer):
        sleep_for = 1
        self._run(target_decorated_function(sleep_for=sleep_for))
        measurement = mocked_buffer.put_nowait.call_args[0][0]  # first element of *args
        self.assertEqual(Measurement, type(measurement))
        created_at, dimensions, metric, unit, value = measurement.created_at, measurement.dimensions, measurement.metric, measurement.unit, measurement.value

        now = datetime.utcnow()
        self.assertTrue(TOLERANCE > abs((now - created_at).total_seconds()))

        self.assertEqual(test_metric, metric)
        self.assertEqual(test_unit, unit)
        self.assertAlmostEqual(sleep_for, value, delta=TOLERANCE)

    def test_multiple_measurements(self, mocked_buffer):
        sleep_for_one, sleep_for_two = 0.3, 0.6

        self._run(target_decorated_function(sleep_for_one))
        now_one = datetime.utcnow()

        sleep(.5)

        self._run(target_decorated_function(sleep_for_two))
        now_two = datetime.utcnow()

        self.assertEqual(2, mocked_buffer.put_nowait.call_count)

        measurement_one = mocked_buffer.put_nowait.call_args_list[0][0][0]
        created_at, dimensions, metric, unit, value = measurement_one.created_at, measurement_one.dimensions, measurement_one.metric, measurement_one.unit, measurement_one.value

        self.assertTrue(TOLERANCE > abs((now_one - created_at).total_seconds()))
        self.assertEqual(test_metric, metric)
        self.assertEqual(test_unit, unit)
        self.assertAlmostEqual(sleep_for_one, value, delta=TOLERANCE)

        measurement_two = mocked_buffer.put_nowait.call_args_list[1][0][0]
        created_at, dimensions, metric, unit, value = measurement_two.created_at, measurement_two.dimensions, measurement_two.metric, measurement_two.unit, measurement_two.value

        self.assertTrue(TOLERANCE > abs((now_two - created_at).total_seconds()))
        self.assertEqual(test_metric, metric)
        self.assertEqual(test_unit, unit)
        self.assertAlmostEqual(sleep_for_two, value, delta=TOLERANCE)

    def test_on_exception_in_target_method(self, mocked_buffer):
        @_ins_test
        async def raising_method():
            raise Exception("some exception")

        with self.assertRaisesRegex(Exception, 'some exception'):
            self._run(raising_method())
        mocked_buffer.put_nowait.assert_called_once()

