import abc
import time
import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect

class StreamType:
    LOCAL_POSITION_NED = 32
    GLOBAL_POSITION = 33
    BATTERY_STATUS = 147
    FENCE_STATUS = 162

class Stream:
    def __init__(self, debug: bool, msg_id: int, time_interval):
        self.debug = debug
        self.msg_id = msg_id
        self.time_interval = time_interval  # in microseconds
        self.prev_time = None

    def log(self, message: str) -> None:
        if self.debug:
            print(message)

    def interval_request(self, connection: utility.mavserial | utility.mavudp) -> None:
        msg = dialect.MAVLink_command_long_message(target_system=connection.target_system,
                                                target_component=connection.target_component,
                                                command=511,  # MAV_CMD_SET_MESSAGE_INTERVAL
                                                confirmation=0,
                                                param1=self.msg_id,
                                                param2=self.time_interval,
                                                param3=0,
                                                param4=0,
                                                param5=0,
                                                param6=0,
                                                param7=0
                                                )
        connection.mav.send(msg)

        self.prev_time = time.time()

    @abc.abstractmethod
    def update(self, connection: utility.mavserial | utility.mavudp) -> None:
        pass

    def is_ready(self) -> bool:
        return (time.time() - self.prev_time) * (10 ** 6) >= self.time_interval
    
    def reset_time(self) -> None:
        self.prev_time = time.time()
