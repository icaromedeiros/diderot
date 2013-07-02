from diderot.utils import parse_facts, difference, get_empty_graph, intersection
from diderot.inference import Inference

import sure


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


def cannot_infer(unexpected_facts):
    """
        Method that initiates the method chaining by constructing an ``UnexpectedInferenceAssertion``
        object with the given unexpected facts.

        .. code-block:: python

           cannot_infer(":Icaro a :Student")

        This function is in ``diderot.__init__``, so it can be imported simply with
        ``from diderot import can_infer``.
    """
    unexpected_facts = parse_facts(unexpected_facts)
    return UnexpectedInferenceAssertion(unexpected_facts=unexpected_facts)


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


class UnexpectedInferenceAssertion(Assertion):
    """
        Class that holds inference assertion values, facts (``rdflib.Graph`` objects),
        with known facts and unexpected inferred facts.

        This class also triggers the inference, on ``inference`` module.
    """

    def __init__(self, unexpected_facts=None, facts=None):
        """
            The constructor for InferenceAssertion generally gets a ``expected_facts`` object as argument,
            as this is the use in ``can_infer`` function.

            Known facts (hereby called ``facts``) can be also passed.

            ``self.assertion_value`` is initialized as ``False``.
        """
        self.unexpected_facts = unexpected_facts
        self.facts = facts
        self.unexpected_inferred_facts = None
        super(UnexpectedInferenceAssertion, self).__init__()

    def from_facts(self, facts):
        """
             This function is part of the method chaining and receives facts as argument,
             so that the inference is triggered using ``self.unexpected_facts`` and ``facts``.

             As part of the method chaining this function returns the object itself, after running the
             inference process, which updates the ``self.assertion_value`` member.

             .. code-block:: python

                cannot_infer(":Icaro a :Student").from_facts(":Icaro a :Human . :Human rdfs:subClassOf :Mortal")
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
        self.unexpected_inferred_facts = intersection(self.unexpected_facts, inferred_facts)
        if self.unexpected_inferred_facts:
            self.assertion_value = False
            self._build_assertion_error_message()
        else:
            self.assertion_value = True

    def _build_assertion_error_message(self):
        """
            Method that builds the AssertionError message.
            All expected and not inferred facts are built in a ``RDFlib.Graphh``
            object and then serialized in NT format.
        """
        ASSERTION_ERROR_MESSAGE = "Could infer some unexpected facts:\n\n  {0}"
        unexpected_facts_graph = get_empty_graph()
        for triple in self.unexpected_inferred_facts:
            unexpected_facts_graph.add(triple)

        self.assertion_error_message = ASSERTION_ERROR_MESSAGE.format(unexpected_facts_graph.serialize(format="nt"))


def can_answer(question):
    """
        Method that initiates the method chaining by constructing an ``CompetencyQuestionAssertion``
        object with a ``SPARQL`` query.

        .. code-block:: python

           can_answer("SELECT ?human WHERE { ?human a <http://example.onto/Human> }")

        This function is in ``diderot.__init__``, so it can be imported simply with
        ``from diderot import can_answer``.
    """
    return CompetencyQuestionAssertion(question)


class CompetencyQuestionAssertion(Assertion):
    """
        Class that holds assertion values for competency question answering.
    """

    def __init__(self, question, ontology_graph=None):
        """
            Write something
        """
        self.question = question
        self.ontology_graph = ontology_graph
        self.query_result = None
        super(CompetencyQuestionAssertion, self).__init__()

    def from_ontology(self, ontology):
        """
            This function is part of the method chaining and receives the ontology as argument.

             .. code-block:: python

                can_answer("SELECT * WHERE {?s ?p ?o}").from_ontology(":Icaro a :Human . :Human rdfs:subClassOf :Mortal")

            If the query to the selected ontology returns ``True`` (for ``ASK`` queries)
            or a non-empty result (for ``SELECT`` queries), ``self.assertion_value`` is set
            to ``True``. Otherwise, ``self.assertion_value`` is set to ``False``.

            If the query is not a ``ASK`` or ``SELECT`` query, a ``RuntimeError`` is raised.

            As part of the method chaining this function returns the object itself.
        """
        ontology_graph = parse_facts(ontology)
        query_result = ontology_graph.query(self.question)
        if query_result.construct:
            raise RuntimeError("Only SELECT or ASK queries are accepted")

        if query_result.askAnswer:
            self.assertion_value = query_result.askAnswer[0]
            if not self.assertion_value:
                ASSERTION_ERROR_MESSAGE = "ASK query returned false.\n  Query: {0}"
                self.assertion_error_message = ASSERTION_ERROR_MESSAGE.format(self.question)
        elif query_result.allVariables is not None:
            self.assertion_value = len(query_result.selected) > 0
            if not self.assertion_value:
                ASSERTION_ERROR_MESSAGE = "SELECT query result is empty.\n  Query: {0}"
                self.assertion_error_message = ASSERTION_ERROR_MESSAGE.format(self.question)
            else:
                self.query_result = query_result
        else:
            raise RuntimeError("Unexpected exception parsing SPARQL query results:\n  {0}".format(self.query_result))

        return self

    def with_answer(self, expected_answers):
        """
            Matches the ``expected_answers`` given as parameter with the ``self.query_result``.

            Note: It is **required** that the expected_answers list of tuples is in the same order
            of the variables passed in the ``SELECT`` query.

            It is also **required** that references to URIs must be passed in ``expected_answers``
            as a ``rdflib.URIRef``.

            .. code-block:: python

                question = \"\"\"
                SELECT ?human ?age ?name
                WHERE {
                    ?human a                          <http://example.onto/Human> ;
                           <http://example.onto/age>  ?age ;
                           <http://example.onto/name> ?name .
                }
                \"\"\"
                expected_answers = [(rdflib.URIRef("http://example.onto/Human"), "Icaro", 26)]
                can_infer(QUESTION).from_ontology(ONTOLOGY).with_answer(expected_answers)

            A ``RuntimeError`` will be raised if:

            * ``expected_answers`` is ``None`` or empty.

            * ``expected_answers`` is not a list of tuples.

            * ``self.query_result`` is ``None`` or empty. This will happen if ``with_answer()`` is called before ``from_ontology()`` or if a non-SELECT query is passed as question to ``can_answer()``.


        """
        if not expected_answers:
            raise RuntimeError("The with_answer() parameter should not be None or empty.")

        if not (isinstance(expected_answers, list) and isinstance(expected_answers[0], tuple)):
            raise RuntimeError("The with_answer() parameter should a list of non-empty tuples.")

        if not self.query_result:
            ERROR_MESSAGE = "Query result is None. Have you called from_ontology() first?\n" + \
                "  The right order is can_answer().from_ontology().with_answer().\n" + \
                "  Also, only SELECT queries are accepted to use with the function with_answer()"
            raise RuntimeError(ERROR_MESSAGE)

        self.assertion_value = False  # rollback assertion value defined in from_ontology

        result_bindings = self.query_result.selected
        try:
            result_bindings.should.be.equal(expected_answers)
        except AssertionError as e:
            self.assertion_value = False
            ASSERTION_ERROR_MESSAGE = "Query result is different from expected answer.\n  " + \
                e.message
            self.assertion_error_message = ASSERTION_ERROR_MESSAGE
        else:
            self.assertion_value = True

        return self
