

class BaseFee:
    def __init__(self, id:int=None):
        if type(id) == int:
            self._load()

    def _load(self):
        raise NotImplementedError()

