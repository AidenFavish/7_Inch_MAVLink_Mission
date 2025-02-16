from mavlink_helper.runners import MainRunner
from mavlink_helper.protocols import ArmProtocol, TakeoffProtocol, ChangeModeProtocol, WaitProtocol, ModeType, CylindricalGeofenceProtocol
import time

runner = MainRunner("udp:127.0.0.1:14550")

# Build the mission
runner.add_action(CylindricalGeofenceProtocol(100.0, 50.0, True))
runner.add_action(WaitProtocol(10.0, debug=True))
runner.add_action(ChangeModeProtocol(ModeType.GUIDED, debug=True))
runner.add_action(ArmProtocol(debug=True))
runner.add_action(TakeoffProtocol(60.0, debug=True))
runner.add_action(WaitProtocol(60.0, debug=True))
runner.add_action(ChangeModeProtocol(ModeType.LAND, debug=True))

runner.start_spinning()
while not runner.finished_actions():
    time.sleep(0.5)
runner.stop_spinning()
print("Mission 1 complete.")
