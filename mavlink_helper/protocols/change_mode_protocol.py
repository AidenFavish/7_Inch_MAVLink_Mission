import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect

from mavlink_helper.protocols import Protocol

class ModeType:
    """Common ArduPilot modes and their value."""
    STABILIZE=0,
    ACRO=1,
    ALT_HOLD=2,
    AUTO=3,
    GUIDED=4,
    LOITER=5,
    RTL=6,
    CIRCLE=7,
    LAND=9,
    DRIFT=11,
    SPORT=13,
    FLIP=14,
    AUTO_TUNE=15,
    POS_HOLD=16,
    BRAKE=17

class ChangeModeProtocol(Protocol):
    def __init__(self, mode: int, debug=False):
        """Changes the vehicles mode. Use ModeType enum for mode value."""
        super().__init__(debug)
        self.mode = mode

    def run(self, connection: utility.mavserial | utility.mavudp) -> None:
        message = dialect.MAVLink_command_long_message(target_system=connection.target_system,
                                                target_component=connection.target_component,
                                                confirmation=0,
                                                command=176,  # MAV_CMD_DO_SET_MODE
                                                param1=1.0,  # Enable custom mode flag
                                                param2=4.0,  # Flightmode number or value
                                                param3=0.0,
                                                param4=0.0, 
                                                param5=0.0, 
                                                param6=0.0, 
                                                param7=0.0)
        
        self.log("Setting mode...")

        connection.mav.send(message)  # Send the mavlink message to the vehicle
        self.log("Set mode message sent. Waiting for ack...")

        # Verify the message was sent with ack
        ack = connection.recv_match(type=dialect.MAVLink_command_ack_message.msgname, blocking=True)
        self.log(f"Set mode ack recieved: {ack}")
