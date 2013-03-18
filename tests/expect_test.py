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


if __name__ == '__main__':
    unittest.main()
