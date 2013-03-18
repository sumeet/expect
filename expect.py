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

    def add_patch(self, obj, method_name, stub):
        patcher = patch.object(obj, method_name, new=stub)
        patcher.start()
        self._patchers.append(patcher)

    def reset(self):
        for patcher in self._patchers:
            patcher.stop()
        del self._patchers[:]


class ExpectCalled(object):

    def __init__(self, obj, expect):
        self._obj = obj
        self._expect = expect

    def stub(self, method_name):
        stub = Stub(method_name)
        default_value = self._expect.make_default_value(method_name)
        stub.set_default_return_value(default_value)
        self._expect.add_patch(self._obj, method_name, stub)
        return StubCalled(stub, self._expect)


class StubCalled(object):

    def __init__(self, stub, expect):
        self._stub = stub
        self._expect = expect

    def and_return(self, return_value):
        self._stub.set_default_return_value(return_value)

    def with_(self, *args, **kwargs):
        default_value = self._expect.make_default_value(self._stub.name)
        args = Args(args, kwargs)
        self._stub.add_return_value(args, default_value)
        self._stub.unset_default_return_value()
        return WithCalled(args, self._stub)


class WithCalled(object):

    def __init__(self, args, stub):
        self._args = args
        self._stub = stub

    def and_return(self, return_value):
        self._stub.unset_default_return_value()
        self._stub.add_return_value(self._args, return_value)
