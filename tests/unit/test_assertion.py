from unittest import TestCase
from mock import patch

from rdflib import RDF, RDFS, URIRef

from marvin import can_infer, OWL
from marvin.utils import get_empty_graph


class InferringExpectedFactsUnitTestCase(TestCase):

    EXPECTED_FACTS = get_empty_graph()
    EXPECTED_FACTS.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
    EXPECTED_FACTS.add((URIRef(":Mortal"), RDF.type, OWL.Class))
    EXPECTED_FACTS.add((URIRef(":Human"), RDF.type, OWL.Class))

    @patch("marvin.assertion.Inference.__init__", return_value=None)
    @patch("marvin.assertion.Inference.add_facts")
    @patch("marvin.assertion.Inference.get_inferred_facts", return_value=EXPECTED_FACTS)
    def test_subclass_assertion(self, get_inferred_facts, add_facts, inference_init):
        facts = get_empty_graph()
        facts.add((URIRef(":Human"), RDFS.subClassOf, URIRef(":Mortal")))
        facts.add((URIRef(":Icaro"), RDF.type, URIRef(":Human")))

        assertion = can_infer(self.EXPECTED_FACTS).from_facts(facts)
        self.assertTrue(assertion.assertion_value)

    @patch("marvin.assertion.Inference.__init__", return_value=None)
    @patch("marvin.assertion.Inference.add_facts")
    @patch("marvin.assertion.Inference.get_inferred_facts", return_value=get_empty_graph())
    def test_subclass_assertion_is_false(self, get_inferred_facts, add_facts, inference_init):
        facts = get_empty_graph()
        facts.add((URIRef(":Human"), RDFS.subClassOf, URIRef(":Mortal")))

        assertion = can_infer(self.EXPECTED_FACTS).from_facts(facts)
        self.assertFalse(assertion.assertion_value)
