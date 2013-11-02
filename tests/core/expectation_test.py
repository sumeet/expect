import unittest

from exam.decorators import fixture
from mock import Mock

from expect.core.args import Args
from expect.core.args import AnyArgs
from expect.core.expectation import Expectation


class ExpectationTestCase(unittest.TestCase):

    obj = fixture(Mock, name='obj', __repr__=lambda self: '<obj>')

    def test_verifies_a_method_was_called_with_the_right_arguments(self):
        expectation = Expectation(self.obj, 'called_method', Args.make(1))
        self.obj.called_method(1)
        expectation.verify()

        expectation = Expectation(self.obj, 'uncalled_method', Args.make(1))
        self.obj.uncalled_method('wrong', 'args')
        try:
            expectation.verify()
        except AssertionError, e:
            self.assertEqual('Expected <obj>.uncalled_method(1) to be called '
                             "but it wasn't.", str(e))
        else:
            raise AssertionError("expected AssertionError")

    def test_verifies_a_method_was_called_with_any_arguments(self):
        expectation = Expectation(self.obj, 'called_method', AnyArgs)
        self.obj.called_method(1, 2, 3, 4, 5, 6)
        expectation.verify()

        expectation = Expectation(self.obj, 'uncalled_method', AnyArgs)
        try:
            expectation.verify()
        except AssertionError, e:
            self.assertEqual('Expected <obj>.uncalled_method(*ANY ARGS) to be '
                             "called but it wasn't.", str(e))
        else:
            raise AssertionError("expected AssertionError")
