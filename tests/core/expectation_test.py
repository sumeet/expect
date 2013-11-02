import unittest

from exam.decorators import fixture

from expect.core.args import Args
from expect.core.args import AnyArgs
from expect.core.expectation import Expectation
from expect.core.stub import Stub


class ExpectationTestCase(unittest.TestCase):

    @fixture
    def stub(self):
        stub = Stub('stub')
        stub.set_default_response('response')
        return stub

    def test_verifies_a_method_was_called_with_the_right_arguments(self):
        expectation = Expectation(self.stub, Args.make(1))
        self.stub(1)
        expectation.verify()

        new_stub = Stub('new_stub')
        new_stub.set_default_response('response')
        expectation = Expectation(new_stub, Args.make(1))
        new_stub('wrong', 'args')
        try:
            expectation.verify()
        except AssertionError, e:
            self.assertEqual("Expected new_stub(1) to be called but it wasn't.",
                             str(e))
        else:
            raise AssertionError("expected AssertionError")

    def test_verifies_a_method_was_called_with_any_arguments(self):
        expectation = Expectation(self.stub, AnyArgs)
        self.stub(1, 2, 3, 4, 5, 6)
        expectation.verify()

        uncalled_stub = Stub('uncalled_stub')
        expectation = Expectation(uncalled_stub, AnyArgs)
        try:
            expectation.verify()
        except AssertionError, e:
            self.assertEqual('Expected uncalled_stub(*ANY ARGS) to be called '
                             "but it wasn't.", str(e))
        else:
            raise AssertionError('expected AssertionError')
