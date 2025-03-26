from mavlink_helper.runners import MainRunner
from mavlink_helper.protocols import ArmProtocol, TakeoffProtocol, ChangeModeProtocol, WaitProtocol, ModeType, PolygonGeofenceProtocol, WaypointMissionProtocol
import time

waypoints = [
    (33.642406884691866, -117.82628696470394, 50.0),
    (33.64248837381376, -117.82646754294689, 50.0),
    (33.64258391268535, -117.82640341235583, 50.0),
    (33.64250523362199, -117.8262312723489, 50.0),
    (33.642406884691866, -117.82628696470394, 50.0),
]

runner = MainRunner("udp:127.0.0.1:14550")

# Build the mission
runner.add_action(PolygonGeofenceProtocol(waypoints))
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
