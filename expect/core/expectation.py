class Expectation(object):

    def __init__(self, stub, call_args):
        self._stub = stub
        self._call_args = call_args

    def verify(self):
        for args in self._stub.was_called_with:
            if self._call_args.matches_args(args):
                return
        raise AssertionError("Expected %s%r to be called but it wasn't." %
                             (self._stub.name, self._call_args))

    def set_call_args(self, args):
        self._call_args = args
