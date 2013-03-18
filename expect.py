from mock import Mock
from mock import patch

from args import Args
from expectation import Expectation
from stub import Stub


def create_new_expect():
    return Expect()


def make_mock(method_name):
    return Mock(name=method_name + '()')


class Expect(object):

    def __init__(self, make_default_value=make_mock):
        self._patchers = []
        self._make_default_value = make_default_value
        self._stubs = {}
        self._expectations = []

    def __call__(self, obj):
        return ExpectCalled(obj, self)

    @property
    def make_default_value(self):
        return self._make_default_value

    def add_patch(self, obj, method_name, stub):
        patcher = patch.object(obj, method_name, side_effect=stub)
        patcher.start()
        self._patchers.append(patcher)

    def add_expectation(self, expectation):
        self._expectations.append(expectation)

    def reset(self):
        for patcher in self._patchers:
            patcher.stop()
        del self._patchers[:]

    def verify(self):
        for expectation in self._expectations:
            expectation.verify()

    def get_stub(self, method_name):
        if method_name not in self._stubs:
            self._stubs[method_name] = Stub(method_name)
        return self._stubs[method_name]


class ExpectCalled(object):

    def __init__(self, obj, expect):
        self._obj = obj
        self._expect = expect
        self._stubs = {}

    def stub(self, method_name):
        stub = self._expect.get_stub(method_name)
        default_value = self._expect.make_default_value(method_name)
        stub.set_default_return_value(default_value)
        self._expect.add_patch(self._obj, method_name, stub)
        return StubCalled(stub, self._expect)

    def should_receive(self, method_name):
        self.stub(method_name)
        expectation = Expectation(self._obj, method_name)
        self._expect.add_expectation(expectation)
        return ShouldReceiveCalled(expectation)


class ShouldReceiveCalled(object):

    def __init__(self, expectation):
        self._expectation = expectation

    def with_(self, *args, **kwargs):
        self._expectation.set_args(Args(args, kwargs))


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
        return StubCalledThenWithCalled(args, self._stub)


class StubCalledThenWithCalled(object):

    def __init__(self, args, stub):
        self._args = args
        self._stub = stub

    def and_return(self, return_value):
        self._stub.unset_default_return_value()
        self._stub.add_return_value(self._args, return_value)
