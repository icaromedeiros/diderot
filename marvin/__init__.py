from unittest import TestCase
from rules import Inference


def can_infer(expected_facts):
    """
    Method that iniates the chaining by constructing an Assertion object
    """
    return Assertion(expected_facts=expected_facts)


class Assertion(object):

    def __init__(self, expected_facts=None, facts=None):
        self.expected_facts = expected_facts
        self.facts = facts
        self.assertion_value = False

    def from_facts(self, facts):
        self.facts = facts
        self._infer()
        return self

    def _infer(self):
        inference = Inference()
        inference.add_facts(self.facts)
        inferred_facts = inference.get_inferred_facts()
        for expected_triple in self.expected_facts.triples((None, None, None)):
            if expected_triple in inferred_facts:
                self.assertion_value = True
            else:
                self.assertion_value = False
                break


class MarvinTestCase(TestCase):

    def assertThat(self, assertion):
        if isinstance(Assertion, assertion):
            pass
        else:
            raise RuntimeError()
