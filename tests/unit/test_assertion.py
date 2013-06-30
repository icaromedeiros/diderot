from unittest import TestCase
from mock import patch, MagicMock

from rdflib import RDF, RDFS, URIRef
from rdflib.sparql.QueryResult import SPARQLQueryResult

from diderot import can_infer, can_answer, OWL
from diderot.utils import get_empty_graph


class InferringExpectedFactsUnitTestCase(TestCase):

    EXPECTED_FACTS = get_empty_graph()
    EXPECTED_FACTS.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
    EXPECTED_FACTS.add((URIRef(":Mortal"), RDF.type, OWL.Class))
    EXPECTED_FACTS.add((URIRef(":Human"), RDF.type, OWL.Class))

    @patch("diderot.assertion.Inference.__init__", return_value=None)
    @patch("diderot.assertion.Inference.add_facts")
    @patch("diderot.assertion.Inference.get_inferred_facts", return_value=EXPECTED_FACTS)
    def test_subclass_assertion(self, get_inferred_facts, add_facts, inference_init):
        facts = get_empty_graph()
        facts.add((URIRef(":Human"), RDFS.subClassOf, URIRef(":Mortal")))
        facts.add((URIRef(":Icaro"), RDF.type, URIRef(":Human")))

        assertion = can_infer(self.EXPECTED_FACTS).from_facts(facts)
        self.assertTrue(assertion.assertion_value)

    @patch("diderot.assertion.Inference.__init__", return_value=None)
    @patch("diderot.assertion.Inference.add_facts")
    @patch("diderot.assertion.Inference.get_inferred_facts", return_value=get_empty_graph())
    def test_subclass_assertion_is_false(self, get_inferred_facts, add_facts, inference_init):
        facts = get_empty_graph()
        facts.add((URIRef(":Human"), RDFS.subClassOf, URIRef(":Mortal")))

        assertion = can_infer(self.EXPECTED_FACTS).from_facts(facts)
        self.assertFalse(assertion.assertion_value)


class AnsweringCompetencyQuestionsUnitTestCase(TestCase):

    def test_result_to_ask_query(self):
        mocked_graph = MagicMock()
        mocked_graph.query = MagicMock(return_value=SPARQLQueryResult(True))
        with patch("diderot.assertion.parse_facts", return_value=mocked_graph):
            assertion = can_answer("ASK { ?s a ?o }").from_ontology("A_ONTOLOGY")
            self.assertTrue(assertion.assertion_value)

    def test_result_to_select_query(self):
        mocked_graph = MagicMock()
        query_result = ([], None, None, None, None, None)
        mocked_graph.query = MagicMock(return_value=SPARQLQueryResult(query_result))  # Empty result
        with patch("diderot.assertion.parse_facts", return_value=mocked_graph):
            assertion = can_answer("SELECT { ?s a ?o }").from_ontology("A_ONTOLOGY")
            self.assertFalse(assertion.assertion_value)

    def test_result_to_construct_query_raises_exception(self):
        mocked_graph = MagicMock()
        mocked_graph.query = MagicMock(return_value=SPARQLQueryResult(get_empty_graph()))  # Graph object
        with patch("diderot.assertion.parse_facts", return_value=mocked_graph):
            try:
                can_answer("SELECT { ?s a ?o }").from_ontology("A_ONTOLOGY")
            except RuntimeError:
                pass
            else:
                self.fail("RuntimeError not raised")

    def test_result_to_construct_unexpected_result_query_raises_exception(self):
        mocked_result = MagicMock()
        mocked_result.construct, mocked_result.selected, mocked_result.askAnswer = (None, None, None)
        mocked_graph = MagicMock()
        mocked_graph.query = MagicMock(return_value=mocked_result)  # Graph object
        with patch("diderot.assertion.parse_facts", return_value=mocked_graph):
            try:
                can_answer("SELECT { ?s a ?o }").from_ontology("A_ONTOLOGY")
            except RuntimeError:
                pass
            else:
                self.fail("RuntimeError not raised")
