TIME_STEP = 0.5 # s
NODE_DISTANCE = 0.01 # m

class Config:
    _shared_state = dict()

    def __init__(self):
        self.__dict__ = self._shared_state

    def __getitem__(self, key):
        return self._shared_state[key]

    def __setitem__(self, key, value):
        self._shared_state[key] = value

Config().TIME_STEP = TIME_STEP
Config().NODE_DISTANCE = NODE_DISTANCE