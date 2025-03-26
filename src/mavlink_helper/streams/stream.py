import time
import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect

class StreamType:
    """Message to tuple(msg_id, receive_msg_name)"""
    LOCAL_POSITION_NED = (32, dialect.MAVLink_local_position_ned_message.msgname)
    GLOBAL_POSITION = (33, dialect.MAVLink_global_position_int_message.msgname)
    BATTERY_STATUS = (147, dialect.MAVLink_battery_status_message.msgname)
    FENCE_STATUS = (162, dialect.MAVLink_fence_status_message.msgname)

class Stream:
    def __init__(self, debug: bool, msg: tuple, time_interval: int):
        self.debug = debug
        self.msg_id = msg[0]
        self.receive_name = msg[1]
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

    def update(self, connection: utility.mavserial | utility.mavudp) -> None:
        """Checks for all pending messages and updates latest_msg attribute, and resets time."""
        self.log(f"Checking for new {self.receive_name}...")

        # Capture all pending messages with receive name
        msg = connection.recv_match(type=self.receive_name)
        temp = msg
        while msg is not None:
            temp = msg
            msg = connection.recv_match(type=self.receive_name)
        msg = temp

        if msg is not None:
            self.log(f"New {self.receive_name} received: {msg}")
            self.latest_msg = msg
            self.reset_time()

    def is_ready(self) -> bool:
        return (time.time() - self.prev_time) * (10 ** 6) >= self.time_interval
    
    def reset_time(self) -> None:
        self.prev_time = time.time()
