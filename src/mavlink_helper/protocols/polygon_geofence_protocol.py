import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect

from mavlink_helper.protocols import Protocol, ParameterProtocol

class PolygonGeofenceProtocol(Protocol):
    def __init__(self, geofence_points: list[float, float], max_altitude: float = 100.0, debug: bool = False):
        """Defines a geofence polygon in lat, lon points and altitude in local meters."""
        super().__init__(debug)
        self.geofence = geofence_points
        self.max_altitude = max_altitude

        # Bitmask that enables max altitude and inclusion/exclusion polygons
        self.param_set_fence_type = ParameterProtocol("FENCE_TYPE", 1 + 4, debug=True)

        self.param_set_max_alt = ParameterProtocol("FENCE_ALT_MAX", self.max_altitude, debug=True)
        self.param_set_fence_action = ParameterProtocol("FENCE_ACTION", 1, debug=True)  # RTL or Land
        self.param_set_fence_enable = ParameterProtocol("FENCE_ENABLE", 1, debug=True)

    def run(self, connection: utility.mavserial | utility.mavudp) -> None:
        ### Clear the fence mission (erase past geofences)
        self.log("Clearing the geofence...")
        message = dialect.MAVLink_mission_clear_all_message(target_system=connection.target_system,
                                                        target_component=connection.target_component,
                                                        mission_type=dialect.MAV_MISSION_TYPE_FENCE)
        connection.mav.send(message)
        # Verify
        message = connection.recv_match(type=dialect.MAVLink_mission_ack_message.msgname, blocking=True)
        self.log(f"Cleared the geofence: {message}")

        ### Send the new fence
        self.log("Sending mission_count...")
        message = dialect.MAVLink_mission_count_message(target_system=connection.target_system,
                                                        target_component=connection.target_component,
                                                        count=len(self.geofence),
                                                        mission_type=dialect.MAV_MISSION_TYPE_FENCE)
        connection.mav.send(message)

        self.log("Sending fence points...")
        seq = 0
        for vertex in self.geofence:
            message = connection.recv_match(type=dialect.MAVLink_mission_request_int_message.msgname, blocking=True)  # Get mission item request
            self.log(f"Recieved mission item request: {message}")
            message = dialect.MAVLink_mission_item_int_message(target_system=connection.target_system,
                                                        target_component=connection.target_component,
                                                        seq=seq,
                                                        frame=dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                                        command=dialect.MAV_CMD_NAV_FENCE_POLYGON_VERTEX_INCLUSION,
                                                        current=0,
                                                        autocontinue=0,
                                                        param1=len(self.geofence),
                                                        param2=0.0,
                                                        param3=0.0,
                                                        param4=0.0,
                                                        x=int(vertex[0] * 1e7),
                                                        y=int(vertex[1] * 1e7),
                                                        z=0,
                                                        mission_type=dialect.MAV_MISSION_TYPE_FENCE)
            connection.mav.send(message)
            seq += 1
        # Verify
        message = connection.recv_match(type=dialect.MAVLink_mission_ack_message.msgname, blocking=True)  # Get mission ack
        self.log(f"Received mission ack: {message}")
        self.log("Completed polygon geofence transfer.")

        self.param_set_fence_type.run_to_completion(connection)
        self.param_set_max_alt.run_to_completion(connection)
        self.param_set_fence_action.run_to_completion(connection)
        self.param_set_fence_enable.run_to_completion(connection)

        self.log("Polygon geofence ready.")
