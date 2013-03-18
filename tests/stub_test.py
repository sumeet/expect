import unittest

from exam.decorators import fixture
from mock import Mock

from stub import Args
from stub import Stub
from stub import UnknownArgumentsError


class StubTestCase(unittest.TestCase):

    stub = fixture(Stub, name='StubName')
    return_value = fixture(Mock, name='return_value')

    def test_can_have_a_return_value_for_specific_arguments(self):
        args = Args.make(1, 2, a='a', b='b')
        self.stub.add_return_value(args, self.return_value)
        self.assertEqual(self.return_value, self.stub(*args.args, **args.kwargs))
        self.assertRaises(UnknownArgumentsError, self.stub, 'other', 'args')

    def test_can_have_a_default_return_value_for_any_arguments(self):
        self.stub.set_default_return_value(self.return_value)
        self.assertEqual(self.return_value, self.stub('any', 'args'))

    def test_repr_shows_its_name(self):
        self.assertEqual("Stub(name='StubName')", repr(self.stub))
