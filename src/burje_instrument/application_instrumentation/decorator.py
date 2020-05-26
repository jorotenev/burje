import logging
import socket
import functools
import time
from contextlib import contextmanager
from datetime import datetime
from burje_instrument.application_instrumentation.transport.buffer import buffer
from burje_instrument.dto import Unit, Measurement

logger = logging.getLogger(__name__)
__all__ = ['Instrumentor']

_default_dimensions = {
    'hostname': socket.gethostname()
}
SENTIMENT = ('__SENTIMENT__',)


class Instrumentor:
    def __init__(self, metric: str, unit: Unit, static_dimensions=None, dynamic_dimensions=None):
        self.metric = metric
        self.unit = unit
        self.static_dimensions = static_dimensions or {}
        self.dynamic_dimensions = dynamic_dimensions or {}

    def report(self, measurement: Measurement):
        buffer.put_nowait(measurement)

    def prepare_measurement(self, value, input_args, input_kwargs, output):
        dynamic = {k: func(input_args, input_kwargs, output) for k, func in self.dynamic_dimensions.items()}
        dimensions = {**_default_dimensions, **dynamic, **self.static_dimensions}
        return Measurement(created_at=datetime.utcnow(), dimensions=dimensions, metric=self.metric, value=value,
                           unit=self.unit)

    def __call__(self, target_func):

        @contextmanager
        def wrapping_logic(*args, **kwargs):
            start_ts = time.time()
            context = {}
            try:
                yield context
            finally:
                context['execution_time'] = round(time.time() - start_ts, 3)

        @functools.wraps(target_func)
        def wrapper(*args, **kwargs):
            async def tmp():
                with wrapping_logic() as time_context:
                    result, target_raised_exception = SENTIMENT, None  # default result of target invocation
                    try:
                        result = (await target_func(*args, **kwargs))
                    except Exception as e:
                        target_raised_exception = e

                try:
                    msr = self.prepare_measurement(input_args=args, input_kwargs=kwargs, output=result,
                                                   value=time_context['execution_time'])
                    self.report(msr)
                except Exception as e:
                    logger.exception(f'Instrumentation of {target_func.__name__} failed.')

                if target_raised_exception:
                    raise target_raised_exception
                else:
                    return result

            return tmp()

        return wrapper
