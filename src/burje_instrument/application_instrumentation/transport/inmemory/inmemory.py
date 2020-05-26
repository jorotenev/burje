from typing import List

from burje_instrument.application_instrumentation.transport.transport import Transport
from burje_instrument.dto import Measurement

in_memory_db = []


class InMemoryTransport(Transport):
    def persist_measurements(self, measurements: List[Measurement]):
        in_memory_db.extend(measurements)
