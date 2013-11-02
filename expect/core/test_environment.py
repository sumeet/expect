from mock import patch


class TestEnvironment(object):

    def __init__(self):
        self._expectations = []
        self._patchers = []

    def add_stub(self, obj, name, stub):
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
