import abc
import pymavlink.mavutil as utility

class Protocol:
    def __init__(self):
        pass

    @abc.abstractmethod
    def run(self, connection: utility.mavserial | utility.mavudp) -> None:
        pass

    def finished(self) -> bool:
        return True
