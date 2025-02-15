import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect
import time

latest_system_time = time.time()

def wait_for_heartbeat(connection: utility.mavserial | utility.mavudp) -> None:
    """Hangs until heartbeat is recieved from connection."""
    connection.wait_heartbeat()

def check_and_send_heartbeat(connection: utility.mavserial | utility.mavudp) -> None:
    """Check if it's time to send a heartbeat and sends it at 1Hz."""
    global latest_system_time
    if time.time() - latest_system_time > 0.99:
        send_single_heartbeat(connection)
        latest_system_time = time.time()

def send_single_heartbeat(connection: utility.mavserial | utility.mavudp) -> None:
    """
    Sends a single heartbeat to connection.
    """
    connection.mav.heartbeat_send(dialect.MAV_TYPE_GCS,  # Type
                                   dialect.MAV_AUTOPILOT_INVALID,  # Set to invalid for compenents that are not flight controllers
                                   0,  # base_mode
                                   0,  # custom_mode
                                   0)  # system_status
