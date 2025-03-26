import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect
from mavlink_helper.streams import Stream, StreamType
from dataclasses import dataclass

@dataclass
class LocalPosition:
    """Local position in NED."""
    timestamp: int  # time since boot in ms
    x: float  # m
    y: float  # m
    z: float  # m
    x_vel: float  # X speed in m/s
    y_vel: float  # Y speed in m/s
    z_vel: float  # Z speed in m/s

class LocalPositionStream(Stream):
    def __init__(self, time_interval, debug=False):
        """Get NED local position at time interval in microseconds."""
        super().__init__(debug, StreamType.LOCAL_POSITION_NED, time_interval)
        self.latest_msg = None
    
    def update(self, connection: utility.mavserial | utility.mavudp) -> None:
        self.log("Checking for new local position...")
        msg = connection.recv_match(type=dialect.MAVLink_local_position_ned_message.msgname)
        if msg is not None:
            self.log(f"New local position received: {msg}")
            self.latest_msg = msg
            self.reset_time()

    def get_position(self) -> LocalPosition:
        return LocalPosition(timestamp=self.latest_msg.time_boot_ms,
                             x=self.latest_msg.x,
                             y=self.latest_msg.y,
                             z=self.latest_msg.z,
                             x_vel=self.latest_msg.vx,
                             y_vel=self.latest_msg.vy,
                             z_vel=self.latest_msg.vz)
