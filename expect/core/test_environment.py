from collections import namedtuple

from mock import patch

from expect.util import falsey_object


class AddedStub(namedtuple('AddedStub', 'obj name stub')):

    def is_for(self, obj, name):
        return obj is self.obj and name == self.name

    def clear_stub_requests(self):
        self.stub.reset()


class TestEnvironment(object):

    def __init__(self):
        self._expectations = []
        self._patchers = []
        self._added_stubs = []

    def find_stub(self, obj, name):
        for added_stub in self._added_stubs:
            if added_stub.is_for(obj, name):
                return added_stub.stub
        return falsey_object('NoStubFound')

    def add_stub(self, obj, name, stub):
        self._added_stubs.append(AddedStub(obj, name, stub))
        patcher = patch.object(obj, name, stub)
        self._patchers.append(patcher)
        patcher.start()

    def reset(self):
        for patcher in self._patchers:
            patcher.stop()

        for added_stub in self._added_stubs:
            added_stub.clear_stub_requests()

        del self._patchers[:]
        del self._expectations[:]

    def add_mock_expectation(self, expectation):
        self._expectations.append(expectation)

    def verify_expectations(self):
        for expectation in self._expectations:
            expectation.verify()
