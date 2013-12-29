from collections import namedtuple

from expect.core.args import AnyArgs
from expect.core.args import Args
from expect.util import falsey_object


class UnknownArgumentsError(Exception):

    def __init__(self, stub, args):
        self._stub = stub
        self._args = args

    def __str__(self):
        return '%s was called with unexpected args %r.' % (self._stub.name,
                                                           self._args)


MethodCall = namedtuple('MethodCall', 'name args')


class StubResponse(namedtuple('StubResponse', 'args return_value')):

    def matches_args(self, args):
        return self.args.matches_args(args)


class Stub(object):

    def __init__(self, name):
        self._name = name
        self._responses = []
        self._requests = []

    def add_response(self, args, return_value):
        self._remove_response(args)
        self._responses.append(StubResponse(args, return_value))

    def set_default_response(self, response):
        self.add_response(AnyArgs, response)

    def remove_default_response(self):
        self._remove_response(AnyArgs)

    def reset(self):
        del self._requests[:]

    def __call__(self, *args, **kwargs):
        args = Args(args, kwargs)
        self._requests.append(args)
        response = self._find_response(args)
        if response:
            return response.return_value
        else:
            raise UnknownArgumentsError(self, args)

    @property
    def name(self):
        return self._name

    @property
    def was_called_with(self):
        return self._requests

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.name)

    def _remove_response(self, args):
        self._responses = [r for r in self._responses if r.args != args]

    def _find_response(self, args):
        for response in self._responses:
            if response.matches_args(args):
                return response
        return falsey_object('NoValueFound')
