from unittest import TestCase
from mock import patch

from rdflib import URIRef

from diderot import DiderotTestCase
from diderot.assertion import InferenceAssertion


class DiderotTestCaseTestCase(TestCase):

    @patch("diderot.case.DiderotTestCase.__init__", return_value=None)
    def test_not_assertion_raises_exception(self, init):
        test_case = DiderotTestCase()
        self.assertRaises(RuntimeError, test_case.assertThat, 1 == 1)

    @patch("diderot.case.DiderotTestCase.__init__", return_value=None)
    def test_false_assertion(self, init):
        test_case = DiderotTestCase()
        false_assertion = InferenceAssertion()
        false_assertion.not_inferred_facts = set([(URIRef(":a"), URIRef(":b"), URIRef(":c"))])
        self.assertRaises(AssertionError, test_case.assertThat, false_assertion)

    @patch("diderot.case.DiderotTestCase.__init__", return_value=None)
    def test_true_assertion(self, init):
        assertion = InferenceAssertion()
        assertion.assertion_value = True
        test_case = DiderotTestCase()
        test_case.assertThat(assertion)
