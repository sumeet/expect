import unittest2

from exam.decorators import fixture

from expect.util import falsey_object


class FalseyObjectTestCase(unittest2.TestCase):

    falsey_obj = fixture(lambda self: falsey_object('UniqueName'))

    def test_is_falsey(self):
        self.assertFalse(self.falsey_obj)

    def test_the_repr_includes_the_name(self):
        self.assertEqual('falsey_object: UniqueName', repr(self.falsey_obj))
