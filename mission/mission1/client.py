from mavlink_helper.runners import MainRunner
import time

runner = MainRunner("")
thread = runner.start_spinning()
time.sleep(5)
runner.stop_spinning()
