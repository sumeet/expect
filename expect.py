from mock import Mock
from mock import patch

from args import Args
from stub import Stub


def create_new_expect():
    return Expect()


def make_mock(method_name):
    return Mock(name=method_name + '()')


class Expect(object):

    def __init__(self, make_default_value=make_mock):
        self._patchers = []
        self._make_default_value = make_default_value

    def __call__(self, obj):
        return ExpectCalled(obj, self)

    @property
    def make_default_value(self):
        return self._make_default_value


class ExpectCalled(object):

    def __init__(self, obj, expect):
        self._obj = obj
        self._expect = expect

    def stub(self, method_name):
        stub = Stub('method_name')
        default_value = self._expect.make_default_value(method_name)
        stub.set_default_return_value(default_value)
        patcher = patch.object(self._obj, method_name, new=stub)
        patcher.start()
        return StubCalled(stub, self._expect)


class StubCalled(object):

    def __init__(self, stub, expect):
        self._stub = stub
        self._expect = expect

    def and_return(self, return_value):
        self._stub.set_default_return_value(return_value)

    def with_(self, *args, **kwargs):
        default_value = self._expect.make_default_value(self._stub.name)
        self._stub.add_return_value(Args(args, kwargs), default_value)
        self._stub.unset_default_return_value()
