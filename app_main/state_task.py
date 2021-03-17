from enum import Enum


class State(Enum):
    Running = 'Running'
    Stop = 'Stop'
    Failed = 'Failed'
