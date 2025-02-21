import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect

from mavlink_helper.protocols import Protocol

class ArmProtocol(Protocol):
    def __init__(self, arm: bool = True, debug: bool = False):
        """Defines a command to arm the drone."""
        super().__init__(debug)
        if arm:
            self.arm = 1.0
        else:
            self.arm = 0.0

    def run(self, connection: utility.mavserial | utility.mavudp) -> None:
        message = dialect.MAVLink_command_long_message(target_system=connection.target_system,
                                                target_component=connection.target_component,
                                                confirmation=0,
                                                command=400,  # MAV_CMD_COMPONENT_ARM_DISARM
                                                param1=self.arm,  # Arm = 1, Disarm = 0
                                                param2=0.0,
                                                param3=0.0,
                                                param4=0.0,
                                                param5=0.0,
                                                param6=0.0,
                                                param7=0.0)
        
        self.log("Arming...")
        connection.mav.send(message)  # Send the mavlink message to the vehicle
        self.log(f"Arming message sent.")

        # Verify the message was sent with ack
        ack = connection.recv_match(type=dialect.MAVLink_command_ack_message.msgname, blocking=True)
        self.log(f"Arming ack recieved: {ack}")
