from expect.util import falsey_object


class ShouldReceiveExpectation(object):

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


# XXX: should we just crash as soon as the method is called instead of in the
# verification step? would probably require mutating Stub.
class ShouldNotReceiveExpectation(object):

    def __init__(self, stub):
        self._stub = stub
        self._call_args = falsey_object('NoCallArgsSet')

    def verify(self):
        if not self._stub.was_called_with:
            return

        if self._stub_was_called_with_specified_args:
            raise AssertionError('Expected %s not to be called with %s, but it '
                                 'was.')

        if self._no_args_were_specified_and_stub_was_called:
            raise AssertionError('Expected %s to not be called, but it was '
                                 'called %d time(s).' %
                                 (self._stub.name,
                                  len(self._stub.was_called_with)))

    def set_call_args(self, args):
        self._call_args = args

    @property
    def _stub_was_called_with_specified_args(self):
        return self._call_args in self._stub.was_called_with

    @property
    def _no_args_were_specified_and_stub_was_called(self):
        return not self._call_args and self._stub.was_called_with
