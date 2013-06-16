from unittest import TestCase

from marvin import MarvinTestCase
from marvin.assertion import Assertion


class MarvinTestCaseTestCase(TestCase):

    def test_not_assertion_raises_exception(self):
        test_case = MarvinTestCase()
        self.assertRaises(RuntimeError, test_case.assertThat, 1 == 1)

    def test_false_assertion(self):
        test_case = MarvinTestCase()
        self.assertRaises(AssertionError, test_case.assertThat, Assertion())

    def test_true_assertion(self):
        assertion = Assertion()
        assertion.assertion_value = True
        test_case = MarvinTestCase()
        test_case.assertThat(assertion)
