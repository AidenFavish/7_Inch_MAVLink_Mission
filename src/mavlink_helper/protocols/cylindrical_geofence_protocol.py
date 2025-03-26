import pymavlink.mavutil as utility
import pymavlink.dialects.v20.all as dialect

from mavlink_helper.protocols import Protocol, ParameterProtocol

class CylindricalGeofenceProtocol(Protocol):
    def __init__(self, radius: float, max_altitude: float, debug: bool = False):
        """
        Defines a cylindrical geofence, radius and height in meters.
        Radius must be greater than 30 meters.
        Max height must be greater than 10 meters.
        Cannot be used in combination with a polygon geofence. (Design decision)
        """
        super().__init__(debug)
        self.radius = radius
        self.max_altitude = max_altitude

        # Bitmask that enables max altitude and circle centered on home fence
        self.param_set_fence_type = ParameterProtocol("FENCE_TYPE", 1 + 2, debug=debug)

        self.param_set_radius = ParameterProtocol("FENCE_RADIUS", self.radius, debug=debug)
        self.param_set_max_alt = ParameterProtocol("FENCE_ALT_MAX", self.max_altitude, debug=debug)
        self.param_set_fence_action = ParameterProtocol("FENCE_ACTION", 1, debug=debug)  # RTL or Land
        self.param_set_fence_enable = ParameterProtocol("FENCE_ENABLE", 1, debug=debug)

    def run(self, connection: utility.mavserial | utility.mavudp) -> None:
        self.log("Setting cylindrical geofence around home position...")

        self.param_set_fence_type.run_to_completion(connection)
        self.param_set_radius.run_to_completion(connection)
        self.param_set_max_alt.run_to_completion(connection)
        self.param_set_fence_action.run_to_completion(connection)
        self.param_set_fence_enable.run_to_completion(connection)

        self.log(f"Radius set to {self.radius} meters, max height set to {self.max_altitude} meters.")
