import mavlink_helper.protocols as protocols

class MainRunner:
    def __init__(self, device: str):
        self.action_list: list[protocols.Protocol] = []
        self.device = device

    def add_action(self, action: protocols.Protocol, index: int | None = None) -> None:
        if index is None:
            self.action_list.append(action)
        else:
            self.action_list.insert(index, action)

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

    def start_spinning(self):
        """Starts up a thread running the main action execution loop."""
        pass  # TODO threading

    def finished_actions(self) -> bool:
        return len(self.action_list) == 0

    def _main_loop(self):
        connection = protocols.get_connection(self.device)  # Get connection
        protocols.wait_for_heartbeat(connection)  # Wait for heartbeat

        while True:
            protocols.check_and_send_heartbeat(connection)

            if not self.finished_actions():
                action_to_run = self.get_next_action()
                action_to_run.run(connection)

                if action_to_run.finished():
                    self.pop_action(0)
