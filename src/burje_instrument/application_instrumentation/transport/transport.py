from abc import ABC, abstractmethod
from typing import List

from burje_instrument.dto import Measurement


class Transport(ABC):
    @classmethod
    def build(cls, *args, **kwargs):
        return cls()

    @abstractmethod
    def persist_measurements(self, measurements: List[Measurement]):
        ...


_transport = None


def get_transport():
    global _transport
    if not _transport:
        # from burje_instrument.application_instrumentation.transport.inmemory.inmemory import InMemoryTransport as T
        from burje_instrument.application_instrumentation.transport.postgres.postgres import PostgresTransport as T

        _transport = T()
    return _transport
