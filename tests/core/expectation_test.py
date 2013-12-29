import re

from exam.decorators import fixture
import unittest2

from expect.core.args import Args
from expect.core.args import AnyArgs
from expect.core.expectation import ShouldNotReceiveExpectation
from expect.core.expectation import ShouldReceiveExpectation
from expect.core.stub import Stub


def create_stub():
    stub = Stub('stub')
    stub.set_default_response('response')
    return stub


class ShouldReceiveExpectationTestCase(unittest2.TestCase):

    stub = fixture(lambda self: create_stub())

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


class ShouldNotReceiveExpectationTestCase(unittest2.TestCase):

    stub = fixture(lambda self: create_stub())
    expectation = fixture(lambda self: ShouldNotReceiveExpectation(self.stub))

    def test_verifies_that_a_stub_was_never_called(self):
        self.expectation.verify()

        self.stub('call with any args')
        self.assertRaises(AssertionError, self.expectation.verify)

    def test_verifies_a_stub_was_not_called_with_specific_arguments(self):
        self.expectation.set_call_args(Args.make(1))

        self.stub('some other args')
        self.expectation.verify()

        self.stub(1)
        with self.assertRaises(AssertionError):
            self.expectation.verify()

    def test_shows_a_useful_error_message_when_the_expectation_fails(self):
        self.stub('call with any args')
        error_msg = ('Expected stub to not be called, but it was called 1 '
                     'time(s).')
        with self.assertRaisesRegexp(AssertionError,
                                     r'^%s$' % re.escape(error_msg)):
            self.expectation.verify()
