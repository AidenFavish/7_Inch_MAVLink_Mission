import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect
from mavlink_helper.streams import Stream, StreamType
from dataclasses import dataclass

@dataclass
class GlobalPosition:
    timestamp: int  # time since boot in ms
    lat: int  # deg * 10^7
    lon: int  # deg * 10^7
    alt: int  # mm in MSL
    relative_alt: int  # mm relative to home
    x_vel: int  # Ground X Speed (Latittude, positive north) cm/s
    y_vel: int  # Ground Y Speed (Longitude, positive east) cm/s
    z_vel: int  # Ground Z Speed (Altitude, positive down) cm/s
    heading: int  # in centi-degrees deg * 10^2, 0 degree north

class GlobalPositionStream(Stream):
    def __init__(self, time_interval, debug=False):
        """Get global position at time interval in microseconds."""
        super().__init__(debug, StreamType.GLOBAL_POSITION, time_interval)
        self.latest_msg = None

    def get_position(self) -> GlobalPosition:
        return GlobalPosition(timestamp=self.latest_msg.time_boot_ms, 
                              lat=self.latest_msg.lat,
                              lon=self.latest_msg.lon,
                              alt=self.latest_msg.alt,
                              relative_alt=self.latest_msg.relative_alt,
                              x_vel=self.latest_msg.vx,
                              y_vel=self.latest_msg.vy,
                              z_vel=self.latest_msg.vz,
                              heading=self.latest_msg.hdg)
