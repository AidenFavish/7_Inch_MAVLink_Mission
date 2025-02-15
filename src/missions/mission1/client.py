from mavlink_helper.runners import MainRunner
from mavlink_helper.protocols import ArmProtocol, TakeoffProtocol, ChangeModeProtocol, WaitProtocol, ModeType
import time

runner = MainRunner("10.0.0.100:14550")

# Build the mission
runner.add_action(ChangeModeProtocol(ModeType.GUIDED, debug=True))
runner.add_action(ArmProtocol(debug=True))
runner.add_action(TakeoffProtocol(10.0, debug=True))
runner.add_action(WaitProtocol(10.0, debug=True))
runner.add_action(ChangeModeProtocol(ModeType.LAND, debug=True))

runner.start_spinning()
while not runner.finished_actions():
    time.sleep(0.5)
runner.stop_spinning()
print("Mission 1 complete.")
