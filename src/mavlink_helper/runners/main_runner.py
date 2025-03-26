import mavlink_helper.protocols as protocols
import mavlink_helper.streams as streams
import threading

class MainRunner:
    def __init__(self, device: str, debug: bool = False):
        self.action_list: list[protocols.Protocol] = []
        self.stream_list: list[streams.Stream] = []
        self.device = device
        self.debug = debug
        self.thread = None
        self.kill_thread = False

    def log(self, message: str):
        if self.debug:
            print(message)

    def add_action(self, action: protocols.Protocol, index: int | None = None) -> protocols.Protocol:
        if index is None:
            self.action_list.append(action)
        else:
            self.action_list.insert(index, action)
        return action

    def remove_action(self, action_type: protocols.Protocol) -> protocols.Protocol:
        for idx, action in enumerate(self.action_list):
            if type(action) == type(action_type):
                self.action_list.pop(idx)
                return action
        raise ValueError("Action type not present.")

    def pop_action(self, index: int) -> protocols.Protocol:
        x = self.action_list.pop(index)
        return x

    def get_action(self, index: int) -> protocols.Protocol:
        return self.action_list[index]

    def get_next_action(self) -> protocols.Protocol:
        return self.get_action(0)

    def get_action_list(self) -> list[protocols.Protocol]:
        return self.action_list

    def set_action_list(self, new_list: list) -> None:
        self.action_list = new_list

    def finished_actions(self) -> bool:
        return len(self.action_list) == 0
    
    def add_stream(self, stream: streams.Stream):
        self.stream_list.append(stream)
        return stream

    def start_spinning(self) -> threading.Thread:
        """Starts up a thread running the main action execution loop."""
        if self.thread is None:
            self.kill_thread = False
            thread = threading.Thread(target=self._main_loop)
            thread.start()
            return thread
        else:
            raise threading.ThreadError("Thread already running!")
        
    def stop_spinning(self):
        self.kill_thread = True

    def manage_streams(self, connection):
        for s in self.stream_list:
            if s.prev_time is None:
                s.interval_request(connection)
            if s.is_ready():
                s.update(connection)

    def _main_loop(self):
        connection = protocols.get_connection(self.device)  # Get connection
        protocols.wait_for_heartbeat(connection)  # Wait for heartbeat
        self.log("\nHeartbeat received and connection established.\n")
        first = True
        while not self.kill_thread:
            protocols.check_and_send_heartbeat(connection)
            self.manage_streams(connection)

            if not self.finished_actions():
                action_to_run = self.get_next_action()

                if first:
                    action_to_run.on_start(connection)

                action_to_run.run(connection)

                if action_to_run.finished():
                    self.pop_action(0)
                    first = True
                else:
                    first = False
