from mavlink_helper.runners import MainRunner
from mavlink_helper.protocols import ArmProtocol, TakeoffProtocol, ChangeModeProtocol, WaitProtocol, ModeType, CylindricalGeofenceProtocol, WaypointMissionProtocol
from mavlink_helper.streams import BatteryStream
import time

runner = MainRunner("udp:10.0.0.100:14550")

# Build the mission
# runner.add_action(CylindricalGeofenceProtocol(30.0,50.0))
runner.add_stream(BatteryStream(100000, True))
runner.add_action(ChangeModeProtocol(ModeType.STABILIZE, debug=True))
runner.add_action(ArmProtocol(debug=True))
# runner.add_action(TakeoffProtocol(25.0, debug=True))
runner.add_action(WaitProtocol(5.0, debug=True))
runner.add_action(ArmProtocol(arm=False, debug=True))
# runner.add_action(ChangeModeProtocol(ModeType.LAND, debug=True))

runner.start_spinning()
while not runner.finished_actions():
    time.sleep(0.5)
runner.stop_spinning()
print("Mission 1 complete.")
