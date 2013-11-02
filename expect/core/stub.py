from collections import namedtuple

from expect.core.args import Args


class UnknownArgumentsError(Exception): pass


MethodCall = namedtuple('MethodCall', 'name args')


class StubResponse(namedtuple('StubResponse', 'args return_value')):

    was_defined = True

    @classmethod
    def default(cls, return_value):
        return cls(cls._no_args, return_value)

    class _no_args(object): pass


class UndefinedStubResponse(object):

    was_defined = False


class Stub(object):

    def __init__(self, name):
        self._name = name
        self._responses = []
        self._default_response = UndefinedStubResponse

    @property
    def name(self):
        return self._name

    def add_response(self, args, response):
        self._remove_response(args)
        self._responses.append(StubResponse(args, response))

    def set_default_response(self, response):
        self._default_response = StubResponse.default(response)

    def __call__(self, *args, **kwargs):
        args = Args(args, kwargs)
        response = self._find_response(args)
        if response.was_defined:
            return response.return_value
        else:
            raise UnknownArgumentsError(args)

    def __repr__(self):
        return '%s(name=%r)' % (type(self).__name__, self.name)

    def _remove_response(self, args):
        self._responses = [r for r in self._responses if r.args != args]

    def _find_response(self, args):
        for return_value in self._responses:
            if return_value.args == args:
                return return_value
        return self._default_response
