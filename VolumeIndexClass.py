class VolumeIndex:
    def __init__(self, idx, volume):
        self.idx = idx
        self.volume = volume
    def __init__(self, **entries):
        self.__dict__.update(entries)