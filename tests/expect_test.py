import unittest

from exam.decorators import fixture
from mock import Mock

from expect import create_new_expect
from stub import UnknownArgumentsError


class ExpectTestCase(unittest.TestCase):

    @fixture
    def obj(self):
        class Obj(object):
            def method(self):
                return 'some_string'
        return Obj()

    expect = fixture(lambda self: create_new_expect())

    def tearDown(self):
        self.expect.reset()

    def test_can_stub_a_method_to_return_a_mock_for_any_arguments(self):
        self.expect(self.obj).stub('method')
        assert isinstance(self.obj.method(), Mock)
        assert isinstance(self.obj.method(1, a=2, b='1234'), Mock)

    def test_can_stub_a_method_to_return_a_mock_for_specific_arguments(self):
        self.expect(self.obj).stub('method').with_(1, a=2, b='1234')
        assert isinstance(self.obj.method(1, a=2, b='1234'), Mock)
        self.assertRaises(UnknownArgumentsError, self.obj.method)

    def test_can_add_custom_return_value_for_any_arguments(self):
        self.expect(self.obj).stub('method').and_return(123)
        self.assertEqual(123, self.obj.method())
        self.assertEqual(123, self.obj.method(1, a=2, b='1234'))

    def test_can_be_reset(self):
        self.expect(self.obj).stub('method')
        self.expect.reset()
        self.assertEqual('some_string', self.obj.method())

    def test_can_add_custom_return_value_for_specific_arguments(self):
        self.expect(self.obj).stub('method').with_(1, a=2).and_return(123)
        self.assertEqual(123, self.obj.method(1, a=2))
        self.assertRaises(UnknownArgumentsError, self.obj.method)

    def test_can_have_separate_return_values_for_different_arguments(self):
        self.expect(self.obj).stub('method').with_('a').and_return(123)
        self.expect(self.obj).stub('method').with_('b').and_return(234)
        self.expect(self.obj).stub('method').with_('c')
        self.expect(self.obj).stub('method')
        self.assertEqual(123, self.obj.method('a'))
        self.assertEqual(234, self.obj.method('b'))
        assert isinstance(self.obj.method('c'), Mock)
        assert isinstance(self.obj.method('d'), Mock)

    def test_raises_exception_if_should_receive_method_but_isnt_called(self):
        self.expect(self.obj).should_receive('method')
        try:
            self.expect.verify()
        except AssertionError, e:
            pass
        message = 'Expected %r.method to be called but it was not' % self.obj
        self.assertEqual(message, str(e))

    def test_does_not_raise_exception_if_should_receive_is_called(self):
        self.expect(self.obj).should_receive('method')
        self.obj.method('any args')
        self.expect.verify()

    def test_should_receive_specific_arguments_raises_exception(self):
        self.expect(self.obj).should_receive('method').with_(1, a=2)
        self.obj.method()
        self.assertRaises(AssertionError, self.expect.verify)

    def test_should_receive_specific_arguments_raises_nothing_when_called(self):
        self.expect(self.obj).should_receive('method').with_(1, a=2)
        self.obj.method(1, a=2)
        self.expect.verify()


if __name__ == '__main__':
    unittest.main()
