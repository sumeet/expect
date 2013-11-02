from collections import namedtuple

from mock import patch

from expect.util import singleton


class AddedStub(namedtuple('AddedStub', 'obj name stub')):

    def is_for(self, obj, name):
        return obj is self.obj and name == self.name


class TestEnvironment(object):

    def __init__(self):
        self._expectations = []
        self._patchers = []
        self._added_stubs = []

    def find_stub(self, obj, name):
        for added_stub in self._added_stubs:
            if added_stub.is_for(obj, name):
                return added_stub.stub
        return NoStubFound

    def add_stub(self, obj, name, stub):
        self._added_stubs.append(AddedStub(obj, name, stub))
        patcher = patch.object(obj, name, stub)
        self._patchers.append(patcher)
        patcher.start()

    def reset_patches(self):
        for patcher in self._patchers:
            patcher.stop()

    def add_mock_expectation(self, expectation):
        self._expectations.append(expectation)

    def verify_expectations(self):
        for expectation in self._expectations:
            expectation.verify()


@singleton
class NoStubFound(object):

    def __nonzero__(self):
        return False
