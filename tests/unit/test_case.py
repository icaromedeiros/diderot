from unittest import TestCase
from mock import patch

from diderot import DiderotTestCase
from diderot.assertion import Assertion


class DiderotTestCaseTestCase(TestCase):

    @patch("diderot.case.DiderotTestCase.__init__", return_value=None)
    def test_not_assertion_raises_exception(self, init):
        test_case = DiderotTestCase()
        self.assertRaises(RuntimeError, test_case.assertThat, 1 == 1)

    @patch("diderot.case.DiderotTestCase.__init__", return_value=None)
    def test_false_assertion(self, init):
        test_case = DiderotTestCase()
        self.assertRaises(AssertionError, test_case.assertThat, Assertion())

    @patch("diderot.case.DiderotTestCase.__init__", return_value=None)
    def test_true_assertion(self, init):
        assertion = Assertion()
        assertion.assertion_value = True
        test_case = DiderotTestCase()
        test_case.assertThat(assertion)
