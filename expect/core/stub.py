from collections import namedtuple

from expect.core.args import AnyArgs
from expect.core.args import Args
from expect.util import singleton


class UnknownArgumentsError(Exception):

    def __init__(self, stub, args):
        self._stub = stub
        self._args = args

    def __str__(self):
        return '%s was called with unexpected args %r.' % (self._stub.name,
                                                           self._args)


MethodCall = namedtuple('MethodCall', 'name args')


StubResponse = namedtuple('StubResponse', 'args return_value')


class Stub(object):

    def __init__(self, name):
        self._name = name
        self._responses = []

    @property
    def name(self):
        return self._name

    def add_response(self, args, response):
        self._remove_response(args)
        self._responses.append(StubResponse(args, response))

    def set_default_response(self, response):
        self.add_response(AnyArgs, response)

    def __call__(self, *args, **kwargs):
        args = Args(args, kwargs)
        response = self._find_response(args)
        if response:
            return response.return_value
        else:
            raise UnknownArgumentsError(self, args)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.name)

    def _remove_response(self, args):
        self._responses = [r for r in self._responses if r.args != args]

    def _find_response(self, args):
        for return_value in self._responses:
            if return_value.args == args:
                return return_value
        return NoValueFound


@singleton
class NoValueFound(object):

    def __nonzero__(self):
        return False
