import abc
import pymavlink.mavutil as utility

class Protocol:
    def __init__(self, debug: bool):
        self.debug = debug

    def log(self, message: str):
        if self.debug:
            print(message)

    def on_start(self, connection: utility.mavserial | utility.mavudp) -> None:
        pass

    @abc.abstractmethod
    def run(self, connection: utility.mavserial | utility.mavudp) -> None:
        pass

    def finished(self) -> bool:
        return True
