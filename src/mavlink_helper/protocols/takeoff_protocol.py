import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect

from mavlink_helper.protocols import Protocol

class TakeoffProtocol(Protocol):
    def __init__(self, takeoff_altitude: float, debug: bool = False):
        """Defines a takeoff command with takeoff altitude in meters."""
        super().__init__(debug)
        self.takeoff_altitude = takeoff_altitude

    def run(self, connection: utility.mavserial | utility.mavudp) -> None:
        message = dialect.MAVLink_command_int_message(target_system=connection.target_system,
                                                target_component=connection.target_component,
                                                frame=3,  # MAV_FRAME_GLOBAL_RELATIVE_ALTITUDE
                                                current=0,
                                                autocontinue=0,
                                                command=22,  # MAV_CMD_NAV_TAKEOFF
                                                param1=0.0,  # Pitch
                                                param2=0.0,
                                                param3=0.0,
                                                param4=0.0,  # Yaw
                                                x=0,  # Lat
                                                y=0,  # Long
                                                z=self.takeoff_altitude)  # Altitude in meters
        
        self.log("Taking off...")
        connection.mav.send(message)  # Send the mavlink message to the vehicle
        self.log(f"Takeoff to {self.takeoff_altitude} meters message sent. Waiting for ack...")

        # Verify the message was sent with ack
        ack = connection.recv_match(type=dialect.MAVLink_command_ack_message.msgname, blocking=True)
        self.log(f"Takeoff ack recieved: {ack}")
