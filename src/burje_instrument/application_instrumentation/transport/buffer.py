from queue import Queue, Empty
from burje_instrument.application_instrumentation.transport.transport import get_transport
from burje_instrument.application_instrumentation.utils import RepeatTimer

buffer = Queue()


def consume_buffer():
    to_send = []

    try:
        for _ in range(100):
            try:
                to_send.append(buffer.get_nowait())
            except Empty as ex:
                break
        if len(to_send):
            get_transport().persist_measurements(to_send)
    except Exception as ex:
        print(str(ex))


timer = RepeatTimer(2, consume_buffer)
timer.start()
