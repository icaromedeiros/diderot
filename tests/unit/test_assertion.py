from unittest import TestCase
from mock import patch, MagicMock

import sure

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
            self.assertIsNone(assertion.assertion_error_message)

    def test_result_to_ask_returns_false(self):
        mocked_graph = MagicMock()
        mocked_graph.query = MagicMock(return_value=SPARQLQueryResult(False))
        with patch("diderot.assertion.parse_facts", return_value=mocked_graph):
            assertion = can_answer("ASK { ?s a ?o }").from_ontology("A_ONTOLOGY")
            self.assertFalse(assertion.assertion_value)
            self.assertIsNotNone(assertion.assertion_error_message)

    def test_result_to_select_query(self):
        mocked_graph = MagicMock()
        # result,selectionF,allVars,orderBy,distinct,topUnion
        query_result = ([("test")], None, ["?s"], None, None, None)
        mocked_graph.query = MagicMock(return_value=SPARQLQueryResult(query_result))  # Non Empty result
        with patch("diderot.assertion.parse_facts", return_value=mocked_graph):
            assertion = can_answer("SELECT { ?s a ?o }").from_ontology("A_ONTOLOGY")
            self.assertTrue(assertion.assertion_value)
            self.assertIsNone(assertion.assertion_error_message)

    def test_result_to_select_query_with_empty_results(self):
        mocked_graph = MagicMock()
        # result,selectionF,allVars,orderBy,distinct,topUnion
        query_result = ([], None, ["?s"], None, None, None)
        mocked_graph.query = MagicMock(return_value=SPARQLQueryResult(query_result))  # Empty result
        with patch("diderot.assertion.parse_facts", return_value=mocked_graph):
            assertion = can_answer("SELECT { ?s a ?o }").from_ontology("A_ONTOLOGY")
            self.assertFalse(assertion.assertion_value)
            self.assertIsNotNone(assertion.assertion_error_message)

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
        mocked_result.construct, mocked_result.allVariables, mocked_result.askAnswer = (None, None, None)
        mocked_graph = MagicMock()
        mocked_graph.query = MagicMock(return_value=mocked_result)  # Graph object
        with patch("diderot.assertion.parse_facts", return_value=mocked_graph):
            try:
                can_answer("SELECT { ?s a ?o }").from_ontology("A_ONTOLOGY")
            except RuntimeError:
                pass
            else:
                self.fail("RuntimeError not raised")

    def test_with_answer_raises_exception_for_empty_expected_answer(self):
        try:
            can_answer("A QUESTION").with_answer([])
        except RuntimeError as e:
            self.assertEqual("The with_answer() parameter should not be None or empty.", e.message)
        else:
            self.fail("RuntimeError not raised")

    def test_with_answer_raises_exception_for_not_list_expected_answer(self):
            try:
                can_answer("A QUESTION").with_answer({"expected_answer": "invalid"})
            except RuntimeError as e:
                self.assertEqual("The with_answer() parameter should a list of non-empty tuples.", e.message)
            else:
                self.fail("RuntimeError not raised")

    def test_with_answer_raises_exception_for_not_list_of_tuples_expected_answer(self):
            try:
                can_answer("A QUESTION").with_answer([{"expected_answer": "invalid"}])
            except RuntimeError as e:
                self.assertEqual("The with_answer() parameter should a list of non-empty tuples.", e.message)
            else:
                self.fail("RuntimeError not raised")

    def test_with_answer_raises_exception_for_empty_query_result(self):
        try:
            can_answer("A QUESTION").with_answer([("test",)])  # Invalid order
        except RuntimeError as e:
            self.assertIn("Query result is None. Have you called from_ontology", e.message)
        else:
            self.fail("RuntimeError not raised")

    def test_with_answer_with_non_select_query(self):
        mocked_graph = MagicMock()
        mocked_graph.query = MagicMock(return_value=SPARQLQueryResult(False))
        with patch("diderot.assertion.parse_facts", return_value=mocked_graph):
            try:
                can_answer("ASK { ?s a ?o }").from_ontology("A_ONTOLOGY").with_answer([("test",)])
            except RuntimeError as e:
                self.assertIn("Query result is None. Have you called from_ontology() first?", e.message)

    def test_with_answer_matches_query_result(self):
        mocked_graph = MagicMock()
        query_result = ([("test",)], None, ["?s"], None, None, None)
        mocked_graph.query = MagicMock(return_value=SPARQLQueryResult(query_result))
        with patch("diderot.assertion.parse_facts", return_value=mocked_graph):
            assertion = can_answer("ASK { ?s a ?o }").from_ontology("A_ONTOLOGY").with_answer([("test",)])
            self.assertTrue(assertion.assertion_value)

    def test_with_answer_does_not_match_query_result(self):
        mocked_graph = MagicMock()
        query_result = ([("test",), ("not_expected_answer",)], None, ["?s"], None, None, None)
        mocked_graph.query = MagicMock(return_value=SPARQLQueryResult(query_result))
        with patch("diderot.assertion.parse_facts", return_value=mocked_graph):
            assertion = can_answer("ASK { ?s a ?o }").from_ontology("A_ONTOLOGY").with_answer([("test",)])
            self.assertFalse(assertion.assertion_value)
            self.assertIn("Query result is different from expected answer", assertion.assertion_error_message)
