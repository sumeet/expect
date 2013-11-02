import unittest

from exam.decorators import fixture
from mock import Mock

from expect.core.stub import UnknownArgumentsError
from expect.ui.expector import Expector


class ExpectorTestCase(unittest.TestCase):

    @fixture
    def my_obj(self):
        class MyObj(object):
            def method(self):
                return 123
            def __repr__(self):
                return 'MyObj'
        return MyObj()

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
