from mavlink_helper.runners import MainRunner
from mavlink_helper.protocols import ArmProtocol, TakeoffProtocol, ChangeModeProtocol, WaitProtocol, ModeType, CylindricalGeofenceProtocol, WaypointMissionProtocol
import time

waypoints = [
    (33.643125569023894, -117.82623647420671, 50.0),
    (33.64323937461924, -117.82571827532405, 50.0),
    (33.64257771207808, -117.82517146423316, 50.0),
    (33.64154547542313, -117.82777053221052, 50.0),
    (33.64519684708034, -117.83001454292969, 50.0),
    (33.64939445347139, -117.82458008167958, 50.0),
    (33.648190502139045, -117.79660909311673, 50.0)
]

runner = MainRunner("udp:127.0.0.1:14550")

# Build the mission
runner.add_action(CylindricalGeofenceProtocol(100.0, 50.0, True))
runner.add_action(WaypointMissionProtocol(waypoints, debug=True))
runner.add_action(WaitProtocol(10.0, debug=True))
runner.add_action(ChangeModeProtocol(ModeType.GUIDED, debug=True))
runner.add_action(ArmProtocol(debug=True))
runner.add_action(TakeoffProtocol(25.0, debug=True))
runner.add_action(WaitProtocol(15.0, debug=True))
runner.add_action(ChangeModeProtocol(ModeType.AUTO, debug=True))
runner.add_action(WaitProtocol(300.0, debug=True))
runner.add_action(ChangeModeProtocol(ModeType.LAND, debug=True))

runner.start_spinning()
while not runner.finished_actions():
    time.sleep(0.5)
runner.stop_spinning()
print("Mission 1 complete.")
