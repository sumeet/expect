import doctest
import unittest2


class READMETestCase(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.doctest_results = doctest.testfile('../README.markdown')

    def test_contains_tests(self):
        self.assertGreater(self.doctest_results.attempted, 0)

    def test_does_not_fail(self):
        self.assertEqual(self.doctest_results.failed, 0)
