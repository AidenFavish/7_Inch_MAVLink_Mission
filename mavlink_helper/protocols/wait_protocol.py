import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect
import time

from mavlink_helper.protocols import Protocol

class WaitProtocol(Protocol):
    def __init__(self, wait_time: float, debug: bool = False):
        """Defines a wait or pause time in seconds."""
        super().__init__(debug)
        self.wait_time = wait_time

    def run(self, connection):
        time.sleep(self.wait_time)
