import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect

from mavlink_helper.protocols import Protocol

class ParameterProtocol(Protocol):
    def __init__(self, param_name: str, param_value: float, debug: bool = False):
        """Defines a protocol to change a parameter."""
        super().__init__(debug)
        self.param_id = param_name.encode(encoding='utf-8')
        self.value = float(param_value)
        self.verified = False

    def on_start(self, connection):
        self.verified = False

    def run(self, connection: utility.mavserial | utility.mavudp) -> None:
        message = dialect.MAVLink_param_set_message(target_system=connection.target_system,
                                                target_component=connection.target_component,
                                                param_id=self.param_id,
                                                param_value=self.value,
                                                param_type=9)  # MAV_PARAM_TYPE_REAL32
        
        self.log(f"Setting parameter: {self.param_id} to {self.value}...")
        connection.mav.send(message)  # Send the mavlink message to the vehicle
        self.log(f"Waiting for confirmation...")

        # Verify the message was sent with ack
        value = connection.recv_match(type=dialect.MAVLink_param_value_message.msgname, blocking=True, timeout=0.5)
        if value is not None:
            self.log(f"Confirmation received: {value}")
            self.verified = True
        else:
            self.log(f"Confirmation not received trying again...")
            self.verified = False

    def finished(self):
        return self.verified
    
    def run_to_completion(self, connection):
        self.on_start(connection)
        while not self.finished():
            self.run(connection)
