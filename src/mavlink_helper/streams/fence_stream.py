import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect
from mavlink_helper.streams import Stream, StreamType
from dataclasses import dataclass

@dataclass
class FenceStatus:
    is_breaching: bool
    number_of_breaches: int
    latest_breach_time: int  # in ms

class FenceStream(Stream):
    def __init__(self, time_interval, debug=False):
        """Get fence status at time interval in microseconds."""
        super().__init__(debug, StreamType.FENCE_STATUS, time_interval)
        self.latest_msg = None

    def get_fence_status(self):
        return FenceStatus(is_breaching=bool(self.latest_msg.breach_status),
                           number_of_breaches=self.latest_msg.breach_count,
                           latest_breach_time=self.latest_msg.breach_time)
