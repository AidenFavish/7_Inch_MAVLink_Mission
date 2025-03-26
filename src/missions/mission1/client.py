from mavlink_helper.runners import MainRunner
from mavlink_helper.protocols import ArmProtocol, TakeoffProtocol, ChangeModeProtocol, WaitProtocol, ModeType, PolygonGeofenceProtocol, WaypointMissionProtocol
from mavlink_helper.streams import GlobalPositionStream, LocalPositionStream, BatteryStream, FenceStream
import time

fence_points = [
    (33.642868, -117.826856),
    (33.642573, -117.826184),
    (33.64306, -117.825836),
    (33.643372, -117.826511),
]

waypoints = [
    (33.6431, -117.82627, 50.0),
    (33.64319, -117.82653, 50.0),
    (33.64287, -117.82669, 50.0),
    (33.6531, -117.82627, 50.0),
]

runner = MainRunner("udp:127.0.0.1:14550")

# Keep track of streams
global_pos = GlobalPositionStream(1000000)
local_pos = LocalPositionStream(1000000)
battery = BatteryStream(1000000)
fence_status = FenceStream(1000000)

# Add streams to runner
runner.add_stream(global_pos)
runner.add_stream(local_pos)
runner.add_stream(battery)
runner.add_stream(fence_status)

### Mission start
runner.add_action(PolygonGeofenceProtocol(fence_points))
runner.add_action(WaypointMissionProtocol(waypoints))
runner.add_action(WaitProtocol(10.0))

runner.add_action(ChangeModeProtocol(ModeType.GUIDED))
runner.add_action(ArmProtocol())
runner.add_action(TakeoffProtocol(25.0))
runner.add_action(WaitProtocol(15.0))

runner.add_action(ChangeModeProtocol(ModeType.AUTO))
runner.add_action(WaitProtocol(300.0))
runner.add_action(ChangeModeProtocol(ModeType.LAND))
### Mission end

# Begin running
runner.start_spinning()
while not runner.finished_actions():
    time.sleep(0.5)
    try:
        print(global_pos.get_position())
        print(local_pos.get_position())
        print(battery.get_batt_remaining())
        print(fence_status.get_fence_status())
    except Exception:
        pass
runner.stop_spinning()
print("Mission 1 complete.")
