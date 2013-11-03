import unittest2

from expect.core.args import Args


class ArgsTestCase(unittest2.TestCase):

    def test_has_a_repr_that_looks_like_call_arguments(self):
        args = Args.make(1, 2, kw1='a string', kw2=3)
        self.assertEqual("(1, 2, kw1='a string', kw2=3)", repr(args))
