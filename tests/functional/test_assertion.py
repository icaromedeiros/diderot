from unittest import TestCase
from rdflib.Graph import Graph
from rdflib import RDF, RDFS, URIRef

from marvin import can_infer, OWL


class InferringFactFromRulesTestCase(TestCase):

    def test_subclass_assertion(self):
        facts = Graph()
        facts.add((URIRef(":Human"), RDFS.subClassOf, URIRef(":Mortal")))
        facts.add((URIRef(":Icaro"), RDF.type, URIRef(":Human")))

        expected_facts = Graph()
        expected_facts.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
        expected_facts.add((URIRef(":Mortal"), RDF.type, OWL.Class))
        expected_facts.add((URIRef(":Human"), RDF.type, OWL.Class))

        assertion = can_infer(expected_facts).from_facts(facts)
        self.assertTrue(assertion.assertion_value)
