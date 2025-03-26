from mavlink_helper.runners import MainRunner
from mavlink_helper.protocols import ArmProtocol, TakeoffProtocol, ChangeModeProtocol, WaitProtocol, ModeType, CylindricalGeofenceProtocol, WaypointMissionProtocol
from mavlink_helper.streams import BatteryStream
import time

runner = MainRunner("udp:127.0.0.1:14550")

# Build the mission
# runner.add_action(CylindricalGeofenceProtocol(30.0,50.0))
batt = runner.add_stream(BatteryStream(1000000, True))
runner.add_action(ChangeModeProtocol(ModeType.POS_HOLD, debug=True))
runner.add_action(ArmProtocol(debug=True))
# runner.add_action(TakeoffProtocol(25.0, debug=True))
runner.add_action(WaitProtocol(5.0, debug=True))
runner.add_action(ArmProtocol(arm=False, debug=True))
# runner.add_action(ChangeModeProtocol(ModeType.LAND, debug=True))

runner.start_spinning()
while not runner.finished_actions():
    time.sleep(0.5)
    if batt.latest_msg is not None:
        print(batt.get_batt_remaining())
runner.stop_spinning()
print("Mission 1 complete.")
