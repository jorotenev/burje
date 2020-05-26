import asyncio
import unittest


class ObsoleteAsyncTestCase(unittest.TestCase):
    loop = asyncio.get_event_loop()

    @classmethod
    def _run(cls, coro):
        return cls.loop.run_until_complete(coro)
