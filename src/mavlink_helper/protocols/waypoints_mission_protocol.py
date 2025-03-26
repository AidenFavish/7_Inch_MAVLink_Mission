import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect

from mavlink_helper.protocols import Protocol

class WaypointMissionProtocol(Protocol):
    def __init__(self, waypoints: list[float, float, float], debug: bool = False):
        """
        Sends a waypoint lap mission plan to flight controlller.
        Does not start mission until mode changed to AUTO.
        waypoints: [lat, long, alt], relative to home position.
        """
        super().__init__(debug)
        self.waypoints = waypoints

    def run(self, connection: utility.mavserial | utility.mavudp) -> None:
        ### Clear the fence mission (erase past geofences)
        self.log("Clearing previous waypoints...")
        message = dialect.MAVLink_mission_clear_all_message(target_system=connection.target_system,
                                                        target_component=connection.target_component,
                                                        mission_type=dialect.MAV_MISSION_TYPE_MISSION)
        connection.mav.send(message)
        # Verify
        message = connection.recv_match(type=dialect.MAVLink_mission_ack_message.msgname, blocking=True)
        self.log(f"Cleared waypoints: {message}")

        ### Send the new fence
        self.log("Sending mission_count...")
        message = dialect.MAVLink_mission_count_message(target_system=connection.target_system,
                                                        target_component=connection.target_component,
                                                        count=len(self.waypoints),
                                                        mission_type=dialect.MAV_MISSION_TYPE_MISSION)
        connection.mav.send(message)

        self.log("Sending waypoints...")
        seq = 0
        for waypoint in self.waypoints:
            message = connection.recv_match(type=dialect.MAVLink_mission_request_message.msgname, blocking=True)  # Get mission item request
            self.log(f"Recieved mission item request: {message}")
            message = dialect.MAVLink_mission_item_int_message(target_system=connection.target_system,
                                                        target_component=connection.target_component,
                                                        seq=seq,
                                                        frame=dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                                        command=dialect.MAV_CMD_NAV_WAYPOINT,
                                                        current=0,
                                                        autocontinue=1,
                                                        param1=0.0,
                                                        param2=0.0,
                                                        param3=0.0,
                                                        param4=0.0,
                                                        x=int(waypoint[0] * 1e7),
                                                        y=int(waypoint[1] * 1e7),
                                                        z=waypoint[2],
                                                        mission_type=dialect.MAV_MISSION_TYPE_MISSION)
            connection.mav.send(message)
            seq += 1
        # Verify
        message = connection.recv_match(type=dialect.MAVLink_mission_ack_message.msgname, blocking=True)  # Get mission ack
        self.log(f"Received mission ack: {message}")
        self.log("Completed waypoints transfer.")
