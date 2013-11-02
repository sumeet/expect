class Expectation(object):

    def __init__(self, stub, call_args):
        self._stub = stub
        self._call_args = call_args

    def verify(self):
        if self._call_args not in self._stub.was_called_with:
            raise AssertionError('Expected %s%r to be called but it '
                                 "wasn't." % (self._stub.name, self._call_args))
