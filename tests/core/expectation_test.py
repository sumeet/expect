import unittest

from exam.decorators import fixture

from expect.core.args import Args
from expect.core.args import AnyArgs
from expect.core.expectation import ShouldReceiveExpectation
from expect.core.stub import Stub


class ShouldReceiveExpectationTestCase(unittest.TestCase):

    @fixture
    def stub(self):
        stub = Stub('stub')
        stub.set_default_response('response')
        return stub

    def test_verifies_a_method_was_called_with_the_right_arguments(self):
        expectation = ShouldReceiveExpectation(self.stub, Args.make(1))
        self.stub(1)
        expectation.verify()

        new_stub = Stub('new_stub')
        new_stub.set_default_response('response')
        expectation = ShouldReceiveExpectation(new_stub, Args.make(1))
        new_stub('wrong', 'args')
        try:
            expectation.verify()
        except AssertionError, e:
            self.assertEqual("Expected new_stub(1) to be called but it wasn't.",
                             str(e))
        else:
            raise AssertionError("expected AssertionError")

    def test_verifies_a_method_was_called_with_any_arguments(self):
        expectation = ShouldReceiveExpectation(self.stub, AnyArgs)
        self.stub(1, 2, 3, 4, 5, 6)
        expectation.verify()

        uncalled_stub = Stub('uncalled_stub')
        expectation = ShouldReceiveExpectation(uncalled_stub, AnyArgs)
        try:
            expectation.verify()
        except AssertionError, e:
            self.assertEqual('Expected uncalled_stub(*ANY ARGS) to be called '
                             "but it wasn't.", str(e))
        else:
            raise AssertionError('expected AssertionError')

    def test_can_set_args_after_object_is_created(self):
        expectation = ShouldReceiveExpectation(self.stub, Args.make(1))
        expectation.set_call_args(AnyArgs)
        self.stub('any args')
        expectation.verify()
