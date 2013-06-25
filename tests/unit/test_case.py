from unittest import TestCase
from mock import patch

from marvin import MarvinTestCase
from marvin.assertion import Assertion


class MarvinTestCaseTestCase(TestCase):

    @patch("marvin.case.MarvinTestCase.__init__", return_value=None)
    def test_not_assertion_raises_exception(self, init):
        test_case = MarvinTestCase()
        self.assertRaises(RuntimeError, test_case.assertThat, 1 == 1)

    @patch("marvin.case.MarvinTestCase.__init__", return_value=None)
    def test_false_assertion(self, init):
        test_case = MarvinTestCase()
        self.assertRaises(AssertionError, test_case.assertThat, Assertion())

    @patch("marvin.case.MarvinTestCase.__init__", return_value=None)
    def test_true_assertion(self, init):
        assertion = Assertion()
        assertion.assertion_value = True
        test_case = MarvinTestCase()
        test_case.assertThat(assertion)
