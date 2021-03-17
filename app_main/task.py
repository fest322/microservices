from state_task import State

class Task:
    def __init__(self, name:str, url: str, interval: float, state: State, task=None):
        self.name = name
        self.url = url
        self.interval = float(interval)
        self.state = state
        self.task = task
