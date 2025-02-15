import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect

from mavlink_helper.protocols import Protocol

class TakeoffProtocol(Protocol):
    def __init__(self, takeoff_altitude: float, debug: bool = False):
        """Defines a takeoff command with takeoff altitude in meters."""
        super().__init__(debug)
        self.takeoff_altitude = takeoff_altitude

    def run(self, connection: utility.mavserial | utility.mavudp) -> None:
        message = dialect.MAVLink_command_long_message(target_system=connection.target_system,
                                                target_component=connection.target_component,
                                                confirmation=0,
                                                command=24,  # MAV_CMD_TAKEOFF_LOCAL
                                                param1=0.0,  # Pitch
                                                param2=0.0,
                                                param3=0.0,  # Ascent rate m/s
                                                param4=0.5,  # Yaw
                                                param5=0.0,  # Y-axis
                                                param6=0.0,  # X-axis
                                                param7=self.takeoff_altitude)  # Z-axis
        
        self.log("Taking off...")
        connection.mav.send(message)  # Send the mavlink message to the vehicle
        self.log(f"Takeoff to {self.takeoff_altitude} meters message sent. Waiting for ack...")

        # Verify the message was sent with ack
        ack = connection.recv_match(type=dialect.MAVLink_command_ack_message.msgname, blocking=True)
        self.log(f"Takeoff ack recieved: {ack}")
