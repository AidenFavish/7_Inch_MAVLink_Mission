import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect

class UnsupportedDeviceConnection(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)

def get_connection(device: str) -> utility.mavserial | utility.mavudp:
    """
    Connects to device either by udp or seriel connection.
    Raises UnsupportedDeviceConnection if connects otherwise.
    """
    connection = utility.mavlink_connection(device=device)
    if type(connection) == utility.mavserial or type(connection) == utility.mavudp:
        raise UnsupportedDeviceConnection
    return connection
