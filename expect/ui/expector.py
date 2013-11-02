from mock import Mock

from expect.core.args import AnyArgs
from expect.core.args import Args
from expect.core.expectation import Expectation
from expect.core.stub import Stub
from expect.core.test_environment import TestEnvironment


class DefaultReturnValueCreator(object):

    @classmethod
    def create(cls, name):
        return Mock(name=name)


class Expector(object):

    def __init__(self, default_return_value_creator=DefaultReturnValueCreator):
        self._test_environment = TestEnvironment()
        self._default_return_value_creator = default_return_value_creator

    def __call__(self, obj):
        return ExpectorWithObj(obj, self._test_environment,
                               self._default_return_value_creator)

    def reset(self):
        self._test_environment.reset_patches()

    def verify(self):
        self._test_environment.verify_expectations()


class ExpectorWithObj(object):
    """The return value of expect(obj)."""

    def __init__(self, obj, test_environment, default_return_value_creator):
        self._obj = obj
        self._test_environment = test_environment
        self._default_return_value_creator = default_return_value_creator

    def stub(self, name):
        stub = self._add_or_find_existing_stub(name)
        default_return_value = self._default_return_value_creator.create(
            stub.name)
        stub.set_default_response(default_return_value)
        return StubExpector(stub, default_return_value)

    def should_receive(self, name):
        stub = self._add_or_find_existing_stub(name)
        expectation = Expectation(stub, AnyArgs)
        self._test_environment.add_mock_expectation(expectation)
        return ShouldReceiveExpector(expectation, self.stub(name))

    def _add_or_find_existing_stub(self, name):
        stub = self._test_environment.find_stub(self._obj, name)
        if stub:
            return stub
        else:
            stub = Stub('%r.%s' % (self._obj, name))
            self._test_environment.add_stub(self._obj, name, stub)
            return stub


class StubExpector(object):
    """The return value of expect(obj).stub('method_name')."""

    def __init__(self, stub, default_return_value):
        self._stub = stub
        self._default_return_value = default_return_value

    def with_(self, *call_args, **call_kwargs):
        self._stub.remove_default_response()
        args = Args(call_args, call_kwargs)
        self._stub.add_response(args, self._default_return_value)
        return StubWithArgsExpector(self._stub, args)

    def and_return(self, return_value):
        self._stub.set_default_response(return_value)


class StubWithArgsExpector(object):
    """The return value of expect(obj).stub('method_name').with_(args)."""

    def __init__(self, stub, args):
        self._stub = stub
        self._args = args

    def and_return(self, return_value):
        self._stub.add_response(self._args, return_value)


class ShouldReceiveExpector(object):
    """The return value of expect(obj).should_receive('method_name')."""

    def __init__(self, expectation, stub_expector):
        self._expectation = expectation
        self._stub_expector = stub_expector

    def with_(self, *args, **kwargs):
        self._expectation.set_call_args(Args(args, kwargs))
        return self._stub_expector.with_(*args, **kwargs)

    def and_return(self, return_value):
        self._stub_expector.and_return(return_value)
