import unittest

from exam.decorators import fixture
from mock import Mock

from expect.core.stub import Args
from expect.core.stub import Stub
from expect.core.stub import UnknownArgumentsError


class StubTestCase(unittest.TestCase):

    stub = fixture(Stub, name='StubName')
    return_value = fixture(Mock, name='return_value')

    def test_can_have_a_return_value_for_specific_arguments(self):
        args = Args.make(1, 2, a='a', b='b')
        self.stub.add_response(args, self.return_value)
        self.assertEqual(self.return_value, self.stub(*args.args,
                                                      **args.kwargs))
        self.assertRaises(UnknownArgumentsError, self.stub, 'other', 'args')

    def test_can_have_a_default_return_value_for_any_arguments(self):
        self.stub.set_default_response(self.return_value)
        self.assertEqual(self.return_value, self.stub('any', 'args'))

    def test_can_have_separate_return_values_for_specific_and_any_args(self):
        args = Args.make(1, 2, a='a', b='b')
        self.stub.add_response(args, self.return_value)

        other_return_value = Mock(name='other_return_value')
        self.stub.set_default_response(other_return_value)

        self.assertEqual(self.return_value, self.stub(*args.args,
                                                      **args.kwargs))
        self.assertEqual(other_return_value, self.stub('any', 'args'))

    def test_repr_shows_its_name(self):
        self.assertEqual("Stub('StubName')", repr(self.stub))

    def test_has_a_helpful_error_message_when_no_return_value_available(self):
        try:
            self.stub('some', 'args')
        except UnknownArgumentsError, e:
            self.assertEqual('StubName was called with unexpected args '
                             "('some', 'args').", str(e))
        else:
            raise AssertionError('expected UnknownArgumentsError')

    def test_records_calls_made_to_it(self):
        self.stub.set_default_response('set so it can be called with any args')
        self.stub('some', 'args')
        self.stub('more args and kwargs', kwarg=1)
        self.assertEqual([Args.make('some', 'args'),
                          Args.make('more args and kwargs', kwarg=1)],
                        self.stub.was_called_with)
