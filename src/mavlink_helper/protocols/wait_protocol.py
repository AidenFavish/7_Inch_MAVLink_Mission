import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect
import time

from mavlink_helper.protocols import Protocol

class WaitProtocol(Protocol):
    def __init__(self, wait_time: float, debug: bool = False):
        """Defines a wait or pause time in seconds."""
        super().__init__(debug)
        self.wait_time = wait_time
        self.done = False

    def on_start(self, connection: utility.mavserial | utility.mavudp) -> None:
        self.start_clock = time.time()
        self.done = False

    def run(self, connection: utility.mavserial | utility.mavudp) -> None:
        if time.time() - self.start_clock >= self.wait_time:
            self.done = True
            self.log("Wait done.")

    def finished(self):
        return self.done
