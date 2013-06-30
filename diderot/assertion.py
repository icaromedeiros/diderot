from diderot.utils import parse_facts, difference, get_empty_graph
from diderot.inference import Inference


def can_infer(expected_facts):
    """
        Method that initiates the method chaining by constructing an ``InferenceAssertion`` object
        with the given expected facts.

        .. code-block:: python

           can_infer(":Icaro a :Mortal")

        This function is in ``diderot.__init__``, so it can be imported simply with
        ``from diderot import can_infer``.
    """
    expected_facts = parse_facts(expected_facts)
    return InferenceAssertion(expected_facts=expected_facts)


class Assertion(object):
    """
        Generic class for assertion
    """

    def __init__(self):
        """
            Initializes assertion_value as ``False`` and assertion_error_message as None.

            These are the two parameters used in client classes, such as ``diderot.DiderotTestCase``.
        """
        self.assertion_value = False
        self.assertion_error_message = None


class InferenceAssertion(Assertion):
    """
        Class that holds inference assertion values, facts (``rdflib.Graph`` objects),
        with known facts and expected inferred facts.

        This class also triggers the inference, on ``inference`` module.
    """

    def __init__(self, expected_facts=None, facts=None):
        """
            The constructor for InferenceAssertion generally gets a ``expected_facts`` object as argument,
            as this is the use in ``can_infer`` function.

            Known facts (hereby called ``facts``) can be also passed.

            ``self.assertion_value`` is initialized as ``False``.
        """
        self.expected_facts = expected_facts
        self.facts = facts
        self.not_inferred_facts = None
        super(InferenceAssertion, self).__init__()

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
        """
            Method that constructs a ``diderot.inference.Inference`` object
            and trigger the inference.
        """
        inference = Inference()
        inference.add_facts(self.facts)
        inferred_facts = inference.get_inferred_facts()
        self.not_inferred_facts = difference(self.expected_facts, inferred_facts)
        if not self.not_inferred_facts:
            self.assertion_value = True
        else:
            self.assertion_value = False
            self._build_assertion_error_message()

    def _build_assertion_error_message(self):
        """
            Method that builds the AssertionError message.
            All expected and not inferred facts are built in a ``RDFlib.Graphh``
            object and then serialized in NT format.
        """
        ASSERTION_ERROR_MESSAGE = "Could not infer some expected facts:\n\n  {0}"
        not_inferred_graph = get_empty_graph()
        for triple in self.not_inferred_facts:
            not_inferred_graph.add(triple)

        self.assertion_error_message = ASSERTION_ERROR_MESSAGE.format(not_inferred_graph.serialize(format="nt"))


def can_answer(question):
    """
        Method that initiates the method chaining by constructing an ``CompetencyQuestionAssertion``
        object with a ``SPARQL`` query.

        .. code-block:: python

           can_answer("SELECT * {}")

        This function is in ``diderot.__init__``, so it can be imported simply with
        ``from diderot import can_answer``.
    """
    return CompetencyQuestionAssertion(question)


class CompetencyQuestionAssertion(Assertion):
    """
        Class that holds assertion values for competency question answering.
    """

    def __init__(self, question, expected_answer=None, ontology_graph=None):
        """
            Write something
        """
        self.question = question
        self.expected_answer = expected_answer
        self.ontology_graph = ontology_graph
        self.query_result = None
        super(CompetencyQuestionAssertion, self).__init__()

    def from_ontology(self, ontology):
        """
            This function is part of the method chaining and receives the ontology as argument.

             As part of the method chaining this function returns the object itself, after running the
             inference process, which updates the ``self.assertion_value`` member.

             .. code-block:: python

                can_infer(":Icaro a :Mortal").from_facts(":Icaro a :Human . :Human rdfs:subClassOf :Mortal")

        """
        ontology_graph = parse_facts(ontology)
        self.query_result = ontology_graph.query(self.question)
        if self.query_result.construct:
            raise RuntimeError("Only SELECT or ASK queries are accepted")

        if self.query_result.askAnswer:
            self.assertion_value = self.query_result.askAnswer[0]
            if not self.assertion_value:
                ASSERTION_ERROR_MESSAGE = "ASK query returned false.\n  Query: {0}"
                self.assertion_error_message = ASSERTION_ERROR_MESSAGE.format(self.question)
        elif self.query_result.selected is not None:
            self.assertion_value = len(self.query_result.selected) > 0
            if not self.assertion_value:
                ASSERTION_ERROR_MESSAGE = "SELECT query result is empty.\n  Query: {0}"
                self.assertion_error_message = ASSERTION_ERROR_MESSAGE.format(self.question)
        else:
            raise RuntimeError("Unexpected exception parsing SPARQL query results:\n  {0}".format(self.query_result))

        return self

    def with_answer(self, expected_answer):
        if not self.query_result.selected:
            raise RuntimeError("Only SELECT queries are accepted to use with with_answer")

        self.assertion_value = False  # rollback assertion value defined in from_ontology
