from utils import parse_facts, is_triples_subset
from rules import Inference


def can_infer(expected_facts):
    """
    Method that iniates the chaining by constructing an Assertion object
    with the given expected facts
    """
    expected_facts = parse_facts(expected_facts)
    return Assertion(expected_facts=expected_facts)


class Assertion(object):
    """
    Class that holds assertion, with known facts
    and expected inferred facts
    """

    def __init__(self, expected_facts=None, facts=None):
        self.expected_facts = expected_facts
        self.facts = facts
        self.assertion_value = False

    def from_facts(self, facts):
        self.facts = parse_facts(facts)
        self._infer()
        return self

    def _infer(self):
        inference = Inference()
        inference.add_facts(self.facts)
        inferred_facts = inference.get_inferred_facts()
        self.assertion_value = is_triples_subset(self.expected_facts, inferred_facts)
