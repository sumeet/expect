import unittest2

from exam.decorators import fixture
from mock import Mock

from expect.core.args import AnyArgs
from expect.core.args import Args
from expect.core.expectation import ShouldReceiveExpectation
from expect.core.stub import Stub
from expect.core.test_environment import TestEnvironment


class TestEnvironmentTestCase(unittest2.TestCase):

    obj = fixture(Mock, name='obj')
    test_environment = fixture(TestEnvironment)

    def test_sets_up_stubs(self):
        stub = Stub('stub')
        stub.set_default_response('response')

        original_methods = [self.obj.method1, self.obj.method2]

        self.test_environment.add_stub(self.obj, 'method1', stub)
        self.test_environment.add_stub(self.obj, 'method2', stub)

        self.assertEqual('response', self.obj.method1('any', 'args'))
        self.assertEqual('response', self.obj.method2('any', 'args'))

        self.test_environment.reset_patches()
        self.assertEqual(original_methods, [self.obj.method1, self.obj.method2])

    def test_verifies_mock_expectations(self):
        stub = Stub('stub')
        stub.set_default_response('response')
        passing_expectation = ShouldReceiveExpectation(stub, AnyArgs)
        failing_expectation = ShouldReceiveExpectation(stub,
                                                       Args.make('some args'))
        self.test_environment.add_mock_expectation(passing_expectation)
        self.test_environment.add_mock_expectation(failing_expectation)
        stub('random args')

        try:
            self.test_environment.verify_expectations()
        except AssertionError, e:
            self.assertEqual("Expected stub('some args') to be called but it "
                             "wasn't.", str(e))
        else:
            raise AssertionError('expected AssertionError')
