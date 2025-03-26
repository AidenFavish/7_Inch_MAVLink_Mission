import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect
from mavlink_helper.streams import Stream, StreamType

class BatteryStream(Stream):
    def __init__(self, time_interval, debug=False):
        """Get battery status at time interval in microseconds."""
        super().__init__(debug, StreamType.BATTERY_STATUS, time_interval)
        self.latest_msg = None
    
    def update(self, connection: utility.mavserial | utility.mavudp) -> None:
        self.log("Checking for new battery status...")
        msg = connection.recv_match(type=dialect.MAVLink_battery_status_message.msgname)
        if msg is not None:
            self.log(f"New battery status found: {msg}")
            self.latest_msg = msg
            self.reset_time()

    def get_batt_remaining(self) -> int:
        """Percent of battery remaining."""
        return self.latest_msg.battery_remaining
