from diderot.utils import parse_facts, is_triples_subset
from diderot.inference import Inference


def can_infer(expected_facts):
    """
        Method that initiates the method chaining by constructing an ``Assertion`` object
        with the given expected facts.

        .. code-block:: python

           can_infer(":Icaro a :Mortal")

        This function is in ``diderot.__init__``, so it can be imported simply with
        ``from diderot import can_infer``.
    """
    expected_facts = parse_facts(expected_facts)
    return Assertion(expected_facts=expected_facts)


class Assertion(object):
    """
        Class that holds assertion values, facts (``rdflib.Graph`` objects),
        with known facts and expected inferred facts.

        This class also triggers the inference, on ``inference`` module.
    """

    def __init__(self, expected_facts=None, facts=None):
        """
            The constructor for Assertion generally gets a ``expected_facts`` object as argument,
            as this is the use in ``can_infer`` function.

            Known facts (hereby called ``facts``) can be also passed.

            ``self.assertion_value`` is initialized as ``False``.
        """
        self.expected_facts = expected_facts
        self.facts = facts
        self.assertion_value = False

    def from_facts(self, facts):
        """
             This function is part of the method chaining and receives facts as argument,
             so that the inference is triggered using ``self.expected_facts`` and ``facts``.

             As part of the method chaining this function returns the object itself, after running the
             inference process, which updates the ``self.assertion_value`` member.

             .. code-block:: python

                can_infer(":Icaro a :Mortal").from_facts(":Icaro a :Human . :Human rdfs:subClassOf :Mortal")
        """
        self.facts = parse_facts(facts)
        self._infer()
        return self

    def _infer(self):
        inference = Inference()
        inference.add_facts(self.facts)
        inferred_facts = inference.get_inferred_facts()
        self.assertion_value = is_triples_subset(self.expected_facts, inferred_facts)
