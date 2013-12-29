import unittest2

from exam.decorators import fixture
from mock import Mock

from expect.core.stub import UnknownArgumentsError
from expect.ui.expector import Expector


class MyObj(object):

    def method(self):
        return 123

    def __repr__(self):
        return 'MyObj'


class StubExpectorTestCase(unittest2.TestCase):

    my_obj = fixture(MyObj)

    def test_stubbing_without_options_returns_default_value(self):
        creator = Mock(name='creator', create=lambda name: name)
        expect = Expector(default_return_value_creator=creator)
        expect(self.my_obj).stub('method')

        self.assertEqual("MyObj.method", self.my_obj.method('any', 'args'))

    def test_stubbing_without_return_value_and_args_returns_default_value(self):
        creator = Mock(name='creator', create=lambda name: 'obj')
        expect = Expector(default_return_value_creator=creator)

        expect(self.my_obj).stub('method').with_('some', 'args')

        self.assertEqual('obj', self.my_obj.method('some', 'args'))
        self.assertRaises(UnknownArgumentsError,
                          lambda: self.my_obj.method('other', 'args'))

    def test_can_stub_without_arguments_with_specific_return_value(self):
        expect = Expector()
        expect(self.my_obj).stub('method').and_return('return_value')
        self.assertEqual('return_value', self.my_obj.method('any', 'args'))
        self.assertEqual('return_value', self.my_obj.method('other', 'args'))

    def test_can_stub_with_specific_arguments_and_specific_return_values(self):
        expect = Expector()
        expect(self.my_obj).stub('method').with_(1).and_return('value 1')
        expect(self.my_obj).stub('method').with_(2).and_return('value 2')

        self.assertEqual('value 1', self.my_obj.method(1))
        self.assertEqual('value 2', self.my_obj.method(2))

        self.assertRaises(UnknownArgumentsError, self.my_obj.method, 'bad args')

    def test_can_stub_equivalent_objects_separately(self):
        # this tests the `is` condition in `AddedStub.is_for`.
        expect = Expector()

        class EquivalentObj(object):
            def stubbable(self):
                return 123
            def __eq__(self, other):
                return True
        obj1, obj2 = EquivalentObj(), EquivalentObj()

        self.assertEqual(obj1, obj2)

        expect(obj1).stub('stubbable').and_return('return_value1')
        expect(obj2).stub('stubbable').and_return('return_value2')

        self.assertEqual('return_value1', obj1.stubbable())
        self.assertEqual('return_value2', obj2.stubbable())

    def test_can_reset_test_environment(self):
        expect = Expector()
        original_method = self.my_obj.method
        expect(self.my_obj).stub('method')
        self.assertNotEqual(original_method, self.my_obj.method)

        expect.reset()
        self.assertEqual(original_method, self.my_obj.method)


class ShouldReceiveExpectorTestCase(unittest2.TestCase):

    my_obj = fixture(MyObj)
    expect = fixture(Expector)

    def test_should_receive_with_no_options_sets_up_an_expectation(self):
        self.expect(self.my_obj).should_receive('method')
        self.assertRaises(AssertionError, self.expect.verify)

        self.my_obj.method()
        self.expect.verify()

    def test_makes_expectations_for_specific_args(self):
        self.expect(self.my_obj).should_receive('method') \
            .with_('specific', 'args')
        self.assertRaises(UnknownArgumentsError,
                          lambda: self.my_obj.method('wrong args'))

        self.assertRaises(AssertionError, self.expect.verify)

        self.my_obj.method('specific', 'args')
        self.expect.verify()

    def test_returns_values_and_makes_expectations_for_any_args(self):
        self.expect(self.my_obj).should_receive('method').and_return('return')
        self.assertEqual('return', self.my_obj.method('any', 'args'))
        self.expect.verify()

    def test_returns_values_and_expects_specific_args(self):
        self.expect(self.my_obj).should_receive('method').with_('args') \
            .and_return('return_value')
        self.assertEqual('return_value', self.my_obj.method('args'))


class ShouldNotReceiveExpectorTestCase(unittest2.TestCase):

    my_obj = fixture(MyObj)
    expect = fixture(Expector)

    # XXX: should we just crash as soon as the method is called instead of in
    # the verification step? would probably require mutating Stub.
    def test_sets_up_should_not_receive_expectations(self):
        self.expect(self.my_obj).should_not_receive('method')
        self.expect.verify()

        self.my_obj.method('any args')
        with self.assertRaises(AssertionError):
            self.expect.verify()

    def test_sets_up_should_not_receive_expectations_with_specific_args(self):
        self.expect(self.my_obj).stub('method')
        self.expect(self.my_obj).should_not_receive('method').with_(1, 2)
        self.my_obj.method('some other args')
        self.expect.verify()

        self.my_obj.method(1, 2)
        with self.assertRaises(AssertionError):
            self.expect.verify()


class ExpectorAssertionsTestCase(unittest2.TestCase):

    assert_equal = fixture(Mock, name='assert_equal')
    expect = fixture(lambda self: Expector(__eq__=self.assert_equal))

    def test_can_delegate_equals(self):
        a, b = Mock(name='a'), Mock(name='b')
        self.expect(a) == b
        self.assert_equal.assert_called_once_with(a, b)
