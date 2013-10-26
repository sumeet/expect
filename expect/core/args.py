from collections import namedtuple


class Args(namedtuple('Args', 'args kwargs')):

    @classmethod
    def make(cls, *args, **kwargs):
        return cls(args, kwargs)
